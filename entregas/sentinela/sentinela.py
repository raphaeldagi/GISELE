#!/usr/bin/env python3
"""SENTINELA: auditoria defensiva de segurança para Android, num arquivo só (Python 3.8+, só biblioteca padrão).

O que ela FAZ
  1. Traz o CATÁLOGO de ameaças ao Android (72 ameaças em 12 famílias), cada uma com os sinais que a denunciam e as defesas que a
     neutralizam, organizado pelas táticas do MITRE ATT&CK Mobile e, nas falhas de app, pelo OWASP Mobile Top 10 (2024).
  2. AUDITA um aparelho seu, ligado por cabo ao computador com a depuração USB autorizada, por meio do `adb`: só comandos de
     LEITURA, numa lista fechada (o executor recusa qualquer outro). Nada é instalado, apagado ou alterado no telefone.
  3. PONTUA cada app de terceiros com uma conta bayesiana (razões de verossimilhança dos sinais, a mesma ideia da decisão
     bayesiana da SYNTHAI) e DECIDE em três níveis: OK, REVISAR (a dúvida é devolvida a você, como o agente da SYNTHAI que
     pergunta ao humano quando errar custa mais que perguntar) e ALTO RISCO.
  4. Explica cada achado com a ameaça que ele indica e o passo a passo da defesa.

O que ela NÃO faz (com a mesma régua)
  - Não é um antivírus residente: roda no computador, sob pedido, e tira uma fotografia do aparelho naquele momento.
  - As razões de verossimilhança são valores de PARTIDA escolhidos por especialista, não medidos num conjunto rotulado; a
    probabilidade impressa é uma ordem de grandeza, não um laudo. Os sinais não são independentes (a lição da Parte 34 da SYNTHAI
    sobre o Naive Bayes), por isso o total é limitado por um teto.
  - Sem lista de indicadores (--ioc), ela não reconhece malware pelo nome. Uma varredura limpa não prova que o aparelho está limpo.
  - Não acessa a internet. Listas de indicadores públicas (por exemplo, a do projeto Echap, github.com/AssoEchap/stalkerware-indicators)
    você baixa e passa com --ioc.

Uso
  python3 sentinela.py --catalogo              lista TODAS as ameaças e TODAS as defesas
  python3 sentinela.py --gerar-md ARQ.md       escreve o catálogo em Markdown
  python3 sentinela.py --auditar               audita o aparelho conectado (adb no PATH)
       [--serial S] [--ioc pacotes.txt|ioc.yaml] [--json saida.json] [--relatorio saida.md]
  python3 sentinela.py --capturar captura.json salva as saídas dos comandos de leitura (para analisar depois, noutro lugar)
  python3 sentinela.py --analisar captura.json analisa uma captura salva
  python3 sentinela.py --demo                  audita um aparelho SIMULADO com problemas plantados
  python3 sentinela.py --testes                roda os testes embutidos
"""

import argparse
import datetime
import json
import math
import re
import shutil
import subprocess
import sys
import unittest

VERSAO = "1.0"

# ======================================================================================================================
# 1. CATÁLOGO DE AMEAÇAS E DEFESAS
# ======================================================================================================================
# Cada ameaça: id, nome, família, tática MITRE ATT&CK Mobile, como acontece, sinais, defesas e referências.
# As táticas usadas são as 12 da matriz Mobile (attack.mitre.org/matrices/mobile): Acesso Inicial, Execução, Persistência,
# Escalada de Privilégio, Evasão de Defesa, Acesso a Credenciais, Descoberta, Movimento Lateral, Coleta, Comando e Controle,
# Exfiltração, Impacto. As falhas de desenvolvimento citam o OWASP Mobile Top 10 de 2024 (M1-M10).

FAMILIAS = {
    "MAL": "Malware e apps maliciosos",
    "ABU": "Abuso de recursos legítimos do Android",
    "ENG": "Engenharia social e golpes",
    "REDE": "Rede e comunicação",
    "TEL": "Telefonia e identidade",
    "SIS": "Sistema, firmware e atualizações",
    "FIS": "Acesso físico e periféricos",
    "PRIV": "Privacidade e rastreamento",
    "CONTA": "Contas e nuvem",
    "APP": "Falhas de apps (OWASP Mobile Top 10 2024)",
    "SUP": "Cadeia de suprimentos",
    "DADO": "Dados no aparelho",
}

AMEACAS = [
    # ---------------------------------------------------------------- MAL
    dict(id="MAL-01", fam="MAL", nome="Trojan bancário com sobreposição (overlay)", tatica="Acesso a Credenciais",
         como="O app desenha uma tela falsa por cima do app do banco e captura senha e token; costuma pedir Acessibilidade para tocar sozinho.",
         sinais=["permissão 'Sobrepor a outros apps' em app sem motivo", "serviço de Acessibilidade ativo em app desconhecido",
                 "pedido insistente de Acessibilidade logo após instalar"],
         defesas=["negar Acessibilidade e Sobreposição a apps que não precisam", "instalar só da Play Store ou loja oficial",
                  "usar o app do banco com biometria e notificação de transação", "Play Protect ligado"],
         refs=["MITRE: Acesso a Credenciais (captura de entrada / sobreposição)"]),
    dict(id="MAL-02", fam="MAL", nome="Spyware comercial e stalkerware", tatica="Coleta",
         como="App instalado por alguém com acesso ao aparelho (ou por exploit) que copia mensagens, localização, chamadas e microfone.",
         sinais=["app sem ícone ou com nome genérico ('Serviço do sistema', 'Wi-Fi')", "administrador do dispositivo desconhecido",
                 "Acessibilidade + leitor de notificações + localização em segundo plano no mesmo app", "bateria e dados móveis altos sem motivo"],
         defesas=["conferir Administradores do dispositivo, Acessibilidade e Acesso a notificações", "comparar com lista de indicadores (--ioc)",
                  "trocar a senha da conta Google de outro aparelho", "em caso de violência doméstica, buscar apoio antes de remover (o agressor percebe)",
                  "restauração de fábrica quando houver dúvida"],
         refs=["Coalition Against Stalkerware", "Echap stalkerware-indicators"]),
    dict(id="MAL-03", fam="MAL", nome="Ransomware e bloqueio de tela", tatica="Impacto",
         como="Cifra arquivos acessíveis ou trava a tela pedindo resgate; usa Administrador do dispositivo para impedir a remoção.",
         sinais=["administrador do dispositivo em app recém-instalado", "Sobreposição permanente", "acesso a todos os arquivos sem motivo"],
         defesas=["backup regular fora do aparelho", "não conceder Administrador do dispositivo", "modo de segurança para desinstalar",
                  "nunca pagar resgate (não garante a devolução)"],
         refs=["MITRE: Impacto"]),
    dict(id="MAL-04", fam="MAL", nome="Fraude de SMS premium e assinaturas (toll fraud)", tatica="Impacto",
         como="Envia SMS pagos ou assina serviços de operadora em segundo plano, interceptando o SMS de confirmação.",
         sinais=["permissões de enviar/ler SMS em app que não é de mensagens", "cobranças desconhecidas na conta da operadora"],
         defesas=["negar SMS a apps que não são o app padrão de mensagens", "pedir bloqueio de serviços premium (VAS) à operadora"],
         refs=["MITRE: Impacto (fraude de cobrança)"]),
    dict(id="MAL-05", fam="MAL", nome="Adware, fraude de cliques e anúncios ocultos", tatica="Impacto",
         como="Abre anúncios fora do app, clica em anúncios em segundo plano, ou esconde o próprio ícone para não ser removido.",
         sinais=["anúncios em tela cheia fora de qualquer app", "app sem ícone no menu", "Sobreposição concedida"],
         defesas=["em Configurações > Apps, ordenar por uso recente e remover o desconhecido", "Play Protect"],
         refs=[]),
    dict(id="MAL-06", fam="MAL", nome="Dropper e carregador (baixa o malware depois)", tatica="Execução",
         como="App aparentemente útil passa na revisão da loja e depois baixa e instala o código malicioso.",
         sinais=["permissão 'Instalar apps desconhecidos' em app que não é loja nem navegador", "pedido de atualização fora da loja"],
         defesas=["negar 'Instalar apps desconhecidos' a todos os apps (liberar só na hora, e revogar)", "Play Protect"],
         refs=["MITRE: Execução / Download de código novo"]),
    dict(id="MAL-07", fam="MAL", nome="Trojan de acesso remoto (RAT)", tatica="Comando e Controle",
         como="Dá ao atacante controle do aparelho: tela, toques, câmera, arquivos; geralmente via Acessibilidade e MediaProjection.",
         sinais=["Acessibilidade em app desconhecido", "ícone de gravação/transmissão de tela aparecendo sozinho"],
         defesas=["remover Acessibilidade de apps desconhecidos", "restauração de fábrica se houver controle remoto confirmado"],
         refs=["MITRE: Comando e Controle"]),
    dict(id="MAL-08", fam="MAL", nome="Mineração de criptomoeda e botnet", tatica="Impacto",
         como="Usa a CPU e a rede do aparelho para minerar ou para ataques a terceiros.",
         sinais=["aquecimento e bateria anormais", "uso de dados em segundo plano alto"],
         defesas=["conferir o uso de bateria e de dados por app", "remover o app suspeito"],
         refs=[]),
    dict(id="MAL-09", fam="MAL", nome="Rootkit e exploit de escalada de privilégio", tatica="Escalada de Privilégio",
         como="Explora falha do kernel ou do sistema para ganhar root e se esconder abaixo dos apps.",
         sinais=["binário su presente sem você ter feito root", "build com chaves de teste", "verificação de boot fora do verde"],
         defesas=["manter o patch de segurança em dia", "restauração de fábrica e reflash da imagem oficial"],
         refs=["MITRE: Escalada de Privilégio"]),
    dict(id="MAL-10", fam="MAL", nome="Apps falsos e reempacotados (clones)", tatica="Acesso Inicial",
         como="Cópia de app famoso, com o mesmo nome e ícone, assinada por outro desenvolvedor e com código malicioso a mais.",
         sinais=["app instalado fora da loja", "desenvolvedor diferente do oficial", "permissões a mais que o original"],
         defesas=["instalar a partir do link oficial do desenvolvedor", "conferir o nome do desenvolvedor na loja"],
         refs=["MITRE: Acesso Inicial"]),
    dict(id="MAL-11", fam="MAL", nome="Golpe de app de empréstimo ou investimento falso", tatica="Coleta",
         como="App financeiro falso coleta contatos e fotos para extorsão, ou mostra lucros fictícios para tomar depósitos.",
         sinais=["app financeiro fora da loja", "permissão de contatos e arquivos em app de empréstimo"],
         defesas=["conferir no órgão regulador se a empresa é autorizada", "negar contatos e fotos"],
         refs=[]),
    # ---------------------------------------------------------------- ABU
    dict(id="ABU-01", fam="ABU", nome="Abuso de Acessibilidade", tatica="Evasão de Defesa",
         como="O serviço de Acessibilidade lê toda a tela e toca por você: é a chave-mestra dos trojans e RATs modernos.",
         sinais=["serviço de Acessibilidade ativo de app que não é de acessibilidade, senha ou automação conhecida"],
         defesas=["Configurações > Acessibilidade > Apps instalados: desligar o que não reconhece", "Android 13+: configurações restritas para apps sideloaded"],
         refs=["MITRE: Evasão de Defesa / Coleta"]),
    dict(id="ABU-02", fam="ABU", nome="Abuso de Administrador do dispositivo", tatica="Persistência",
         como="Com Administrador, o app pode travar a tela, apagar dados e dificultar a desinstalação.",
         sinais=["administrador do dispositivo que não é Encontre Meu Dispositivo nem gestão da empresa"],
         defesas=["Configurações > Segurança > Apps de administração do dispositivo: desativar e depois desinstalar"],
         refs=["MITRE: Persistência"]),
    dict(id="ABU-03", fam="ABU", nome="Leitor de notificações (rouba códigos 2FA e mensagens)", tatica="Coleta",
         como="O acesso a notificações lê todo SMS, código de verificação e mensagem que aparece na barra.",
         sinais=["acesso a notificações concedido a app que não é relógio, carro ou assistente conhecido"],
         defesas=["Configurações > Notificações > Acesso a notificações: revogar", "preferir app autenticador ou chave de segurança a SMS"],
         refs=["MITRE: Coleta"]),
    dict(id="ABU-04", fam="ABU", nome="Sobreposição e tapjacking", tatica="Acesso a Credenciais",
         como="Uma janela por cima engana o toque: você pensa que toca em 'Cancelar' e concede uma permissão.",
         sinais=["'Sobrepor a outros apps' concedido a app sem motivo"],
         defesas=["Configurações > Apps > Acesso especial > Sobrepor a outros apps: revogar"],
         refs=["OWASP M8"]),
    dict(id="ABU-05", fam="ABU", nome="Teclado malicioso (keylogger)", tatica="Acesso a Credenciais",
         como="Um teclado de terceiros vê tudo o que você digita, inclusive senhas.",
         sinais=["teclado padrão que não é o do fabricante nem o Gboard/SwiftKey"],
         defesas=["usar o teclado do sistema", "remover teclados não usados em Idiomas e entrada"],
         refs=["MITRE: Acesso a Credenciais (captura de entrada)"]),
    dict(id="ABU-06", fam="ABU", nome="Captura e transmissão de tela (MediaProjection)", tatica="Coleta",
         como="O app grava ou transmite a tela, incluindo senhas e mensagens.",
         sinais=["indicador de gravação de tela aparecendo sem você pedir"],
         defesas=["negar a captura quando não foi você que pediu", "revisar os indicadores de privacidade (Android 12+)"],
         refs=["MITRE: Coleta (captura de tela)"]),
    dict(id="ABU-07", fam="ABU", nome="Instalação de fontes desconhecidas (sideload)", tatica="Acesso Inicial",
         como="App com 'Instalar apps desconhecidos' pode instalar outros apps sem passar pela loja.",
         sinais=["apps com 'Instalar apps desconhecidos' permitido", "apps cujo instalador não é uma loja"],
         defesas=["revogar 'Instalar apps desconhecidos' de todos", "Play Protect verificando apps instalados por USB"],
         refs=["MITRE: Acesso Inicial"]),
    dict(id="ABU-08", fam="ABU", nome="Excesso de permissões perigosas", tatica="Coleta",
         como="Câmera, microfone, localização em segundo plano, SMS, registro de chamadas e contatos em app que não precisa.",
         sinais=["app com SMS, chamadas, microfone e localização juntos"],
         defesas=["Painel de privacidade e Gerenciador de permissões: revogar", "remover permissões de apps não usados (automático no Android 11+)"],
         refs=["OWASP M6"]),
    dict(id="ABU-09", fam="ABU", nome="Sequestro de tarefa e de intent (StrandHogg e afins)", tatica="Evasão de Defesa",
         como="App malicioso se insere na pilha de telas de um app legítimo ou intercepta intents implícitos.",
         sinais=["tela de login aparece de novo logo após abrir um app legítimo"],
         defesas=["manter o Android atualizado", "desenvolvedores: taskAffinity vazio, intents explícitos, componentes não exportados"],
         refs=["OWASP M8"]),
    # ---------------------------------------------------------------- ENG
    dict(id="ENG-01", fam="ENG", nome="Phishing por SMS (smishing) e mensageiros", tatica="Acesso Inicial",
         como="Mensagem urgente (entrega, banco, multa) com link para página falsa ou APK.",
         sinais=["link encurtado ou domínio parecido com o oficial", "pedido de instalar app por link"],
         defesas=["nunca instalar app por link de mensagem", "abrir o site digitando o endereço oficial", "filtro de spam do app de mensagens"],
         refs=["MITRE: Acesso Inicial (phishing)"]),
    dict(id="ENG-02", fam="ENG", nome="Ligação falsa (vishing) e falsa central", tatica="Acesso a Credenciais",
         como="Golpista se passa pelo banco e pede código, senha ou para instalar app de 'proteção' ou acesso remoto.",
         sinais=["pedido de código recebido por SMS", "pedido de instalar app de acesso remoto"],
         defesas=["banco não pede código nem senha por telefone: desligar e ligar para o número oficial", "nunca instalar app de acesso remoto a pedido"],
         refs=[]),
    dict(id="ENG-03", fam="ENG", nome="QR code malicioso (quishing)", tatica="Acesso Inicial",
         como="QR code colado sobre o legítimo leva a site falso ou a download de APK.",
         sinais=["QR em adesivo sobreposto", "endereço exibido diferente do esperado"],
         defesas=["conferir o endereço antes de abrir", "não instalar apps a partir de QR"],
         refs=[]),
    dict(id="ENG-04", fam="ENG", nome="Falso suporte e apps de acesso remoto", tatica="Comando e Controle",
         como="Golpista convence a vítima a instalar um app legítimo de acesso remoto e opera o aparelho.",
         sinais=["app de acesso remoto instalado recentemente sem uso seu"],
         defesas=["desinstalar apps de acesso remoto que não usa", "nunca dar código de sessão a quem ligou"],
         refs=[]),
    dict(id="ENG-05", fam="ENG", nome="Golpe de engenharia social em redes e marketplaces", tatica="Acesso Inicial",
         como="Perfil falso, falsa venda ou falso emprego que leva a pagamento, código ou instalação.",
         sinais=["pressa e pagamento fora da plataforma"],
         defesas=["negociar só dentro da plataforma", "desconfiar de urgência"],
         refs=[]),
    # ---------------------------------------------------------------- REDE
    dict(id="REDE-01", fam="REDE", nome="Homem no meio em Wi-Fi público ou falso (evil twin)", tatica="Coleta",
         como="Rede com o mesmo nome de uma conhecida intercepta ou altera o tráfego não cifrado.",
         sinais=["aviso de certificado inválido", "rede aberta com nome de estabelecimento"],
         defesas=["preferir dados móveis ou VPN confiável em rede pública", "esquecer redes abertas", "nunca aceitar certificado inválido"],
         refs=["OWASP M5"]),
    dict(id="REDE-02", fam="REDE", nome="Certificado CA instalado pelo usuário (interceptação TLS)", tatica="Coleta",
         como="Um certificado raiz extra permite decifrar o tráfego de apps que confiam em certificados do usuário.",
         sinais=["'Credenciais do usuário' com certificado que você não instalou", "aviso 'a rede pode estar sendo monitorada'"],
         defesas=["Configurações > Segurança > Criptografia e credenciais > Credenciais do usuário: remover o desconhecido"],
         refs=["OWASP M5"]),
    dict(id="REDE-03", fam="REDE", nome="Proxy HTTP global configurado", tatica="Coleta",
         como="Proxy definido no sistema encaminha o tráfego por um servidor de terceiros.",
         sinais=["proxy global definido nas configurações"],
         defesas=["remover o proxy em Wi-Fi > rede > Proxy", "via adb: settings put global http_proxy :0 (só se foi você que definiu)"],
         refs=["OWASP M5"]),
    dict(id="REDE-04", fam="REDE", nome="Sequestro de DNS", tatica="Coleta",
         como="Roteador ou rede comprometida responde endereços falsos para sites legítimos.",
         sinais=["sites conhecidos pedindo login de novo ou com certificado estranho"],
         defesas=["ativar DNS privado (DNS sobre TLS) em Configurações > Rede > DNS particular"],
         refs=["OWASP M5"]),
    dict(id="REDE-05", fam="REDE", nome="VPN maliciosa ou gratuita que vende dados", tatica="Exfiltração",
         como="O app de VPN vê todo o tráfego e pode registrar ou injetar conteúdo.",
         sinais=["VPN desconhecida ativa", "chave de VPN na barra de status sem você ter ligado"],
         defesas=["usar só VPN de fornecedor confiável", "remover VPNs que não usa"],
         refs=[]),
    dict(id="REDE-06", fam="REDE", nome="Ataques por Bluetooth", tatica="Movimento Lateral",
         como="Falhas na pilha Bluetooth ou emparelhamentos indevidos permitem acesso ou rastreamento.",
         sinais=["dispositivos emparelhados que você não reconhece"],
         defesas=["desligar Bluetooth quando não usa", "remover pareamentos desconhecidos", "manter o patch em dia"],
         refs=["MITRE: Movimento Lateral"]),
    dict(id="REDE-07", fam="REDE", nome="NFC: retransmissão e leitura indevida", tatica="Coleta",
         como="Ataque de relay usa o NFC do aparelho ou do cartão para pagamento à distância curta.",
         sinais=["NFC sempre ligado", "app de pagamento desconhecido como padrão"],
         defesas=["desligar NFC quando não usa", "exigir desbloqueio para pagamento por aproximação"],
         refs=[]),
    dict(id="REDE-08", fam="REDE", nome="Exploit sem clique (zero-click) por mensagem ou mídia", tatica="Execução",
         como="Arquivo de mídia ou mensagem malformada explora falha no processamento sem interação.",
         sinais=["difícil de ver: o melhor sinal é patch atrasado"],
         defesas=["patch de segurança em dia", "atualizar apps de mensagem", "Modo de Proteção Avançada (Android 16) para quem é alvo"],
         refs=["MITRE: Execução"]),
    # ---------------------------------------------------------------- TEL
    dict(id="TEL-01", fam="TEL", nome="Troca de chip (SIM swap)", tatica="Acesso a Credenciais",
         como="Golpista transfere o seu número para outro chip e recebe os códigos por SMS.",
         sinais=["sinal de operadora some de repente", "aviso de troca de chip"],
         defesas=["PIN do chip", "pedir à operadora bloqueio de portabilidade e troca", "2FA por app ou chave, não SMS"],
         refs=[]),
    dict(id="TEL-02", fam="TEL", nome="Estação rádio-base falsa (IMSI catcher) e rebaixamento para 2G", tatica="Coleta",
         como="Antena falsa força o aparelho a 2G para interceptar chamadas e SMS.",
         sinais=["aparelho caindo para 2G em área com 4G/5G"],
         defesas=["desligar 2G em Rede móvel (Android 12+ em muitos aparelhos)"],
         refs=[]),
    dict(id="TEL-03", fam="TEL", nome="Interceptação por SS7 e SMS como segundo fator", tatica="Acesso a Credenciais",
         como="Falhas da sinalização entre operadoras permitem desviar SMS.",
         sinais=["códigos de verificação que você não pediu"],
         defesas=["trocar SMS por app autenticador ou chave de acesso (passkey)"],
         refs=[]),
    dict(id="TEL-04", fam="TEL", nome="Desvio de chamadas configurado sem você saber", tatica="Coleta",
         como="Códigos de operadora desviam chamadas (inclusive de verificação de banco) para outro número.",
         sinais=["chamadas não chegam", "ícone de desvio ativo"],
         defesas=["conferir e cancelar desvios no discador (Configurações de chamada)"],
         refs=[]),
    # ---------------------------------------------------------------- SIS
    dict(id="SIS-01", fam="SIS", nome="Patch de segurança desatualizado", tatica="Escalada de Privilégio",
         como="Falhas já públicas e corrigidas continuam exploráveis no aparelho sem atualização.",
         sinais=["nível de patch com mais de 90 dias"],
         defesas=["Configurações > Sistema > Atualização de software", "atualizações do Google Play (sistema)"],
         refs=["Boletins de segurança do Android"]),
    dict(id="SIS-02", fam="SIS", nome="Aparelho sem suporte (fim de vida)", tatica="Escalada de Privilégio",
         como="O fabricante parou de publicar correções: toda falha nova fica aberta para sempre.",
         sinais=["patch com mais de um ano", "versão do Android antiga"],
         defesas=["trocar o aparelho ou usar ROM mantida e auditada", "reduzir apps e dados sensíveis nele"],
         refs=[]),
    dict(id="SIS-03", fam="SIS", nome="Bootloader desbloqueado", tatica="Persistência",
         como="Permite gravar sistema modificado; quem pega o aparelho pode trocar o sistema.",
         sinais=["verificação de boot laranja", "ro.boot.flash.locked = 0"],
         defesas=["rebloquear o bootloader com a imagem oficial (apaga os dados: fazer backup)"],
         refs=[]),
    dict(id="SIS-04", fam="SIS", nome="Root (su, Magisk, KernelSU)", tatica="Escalada de Privilégio",
         como="Qualquer app com root lê tudo; malware explora root já existente.",
         sinais=["binário su", "app gerenciador de root instalado"],
         defesas=["remover o root se não for indispensável", "se mantiver, conceder root a pouquíssimos apps"],
         refs=[]),
    dict(id="SIS-05", fam="SIS", nome="Firmware de origem duvidosa ou com chaves de teste", tatica="Persistência",
         como="Aparelhos baratos ou ROMs não oficiais vêm com malware de fábrica ou assinatura de teste.",
         sinais=["ro.build.tags = test-keys", "ro.debuggable = 1 num aparelho de usuário"],
         defesas=["reinstalar firmware oficial", "preferir aparelhos com Google Play Protect certificado"],
         refs=["OWASP M2"]),
    dict(id="SIS-06", fam="SIS", nome="Armazenamento sem criptografia", tatica="Coleta",
         como="Sem criptografia, quem tira o armazenamento lê os dados.",
         sinais=["ro.crypto.state diferente de encrypted"],
         defesas=["criptografia vem ligada no Android 10+; em aparelhos antigos, ativar em Segurança"],
         refs=[]),
    dict(id="SIS-07", fam="SIS", nome="Play Protect desligado", tatica="Evasão de Defesa",
         como="Sem a verificação, apps maliciosos conhecidos não são bloqueados nem removidos.",
         sinais=["verificação de apps desligada"],
         defesas=["Play Store > Play Protect > Configurações: ligar 'Verificar apps'"],
         refs=[]),
    # ---------------------------------------------------------------- FIS
    dict(id="FIS-01", fam="FIS", nome="Perda ou roubo do aparelho", tatica="Acesso Inicial",
         como="Quem tem o aparelho tenta desbloquear, trocar o chip e redefinir contas.",
         sinais=["(físico)"],
         defesas=["bloqueio de tela forte", "Encontre Meu Dispositivo ligado", "Proteção contra roubo do Google (bloqueio por detecção de roubo)",
                  "PIN do chip", "anotar o IMEI"],
         refs=[]),
    dict(id="FIS-02", fam="FIS", nome="Sem bloqueio de tela ou bloqueio fraco", tatica="Acesso Inicial",
         como="Qualquer pessoa com o aparelho na mão instala spyware em minutos.",
         sinais=["bloqueio de tela desativado", "padrão simples ou PIN curto"],
         defesas=["PIN de 6+ dígitos ou senha", "tempo de bloqueio curto", "esconder notificações sensíveis na tela de bloqueio"],
         refs=[]),
    dict(id="FIS-03", fam="FIS", nome="Depuração USB (ADB) e Opções do desenvolvedor ligadas", tatica="Acesso Inicial",
         como="Com ADB ligado, um computador autorizado instala e lê apps sem passar pela loja.",
         sinais=["adb_enabled = 1 fora de uma sessão de uso seu"],
         defesas=["desligar a depuração USB depois desta auditoria", "revogar autorizações de depuração USB"],
         refs=[]),
    dict(id="FIS-04", fam="FIS", nome="Carregador ou cabo malicioso (juice jacking)", tatica="Acesso Inicial",
         como="Porta de carregamento pública troca dados com o aparelho.",
         sinais=["pedido de 'confiar neste computador' ao carregar"],
         defesas=["usar carregador próprio", "bloqueador de dados USB", "manter 'só carregar' como padrão USB"],
         refs=[]),
    dict(id="FIS-05", fam="FIS", nome="Acesso de pessoa próxima (parceiro, colega)", tatica="Acesso Inicial",
         como="Quem conhece o desbloqueio instala stalkerware ou lê conversas.",
         sinais=["biometria de outra pessoa cadastrada", "apps desconhecidos"],
         defesas=["trocar o PIN", "conferir digitais e rostos cadastrados", "Verificação de segurança do Google"],
         refs=[]),
    # ---------------------------------------------------------------- PRIV
    dict(id="PRIV-01", fam="PRIV", nome="Rastreamento de localização", tatica="Coleta",
         como="Apps com localização em segundo plano reconstroem a sua rotina.",
         sinais=["localização 'Permitir o tempo todo' em vários apps"],
         defesas=["localização 'Só durante o uso' ou 'Perguntar'", "localização aproximada quando bastar"],
         refs=["OWASP M6"]),
    dict(id="PRIV-02", fam="PRIV", nome="Rastreador físico escondido (tag Bluetooth)", tatica="Coleta",
         como="Tag de rastreamento colocada na bolsa ou no carro.",
         sinais=["alerta de rastreador desconhecido"],
         defesas=["manter os alertas de rastreadores desconhecidos ligados", "fazer a varredura manual de rastreadores"],
         refs=[]),
    dict(id="PRIV-03", fam="PRIV", nome="SDKs de publicidade e corretores de dados", tatica="Exfiltração",
         como="Bibliotecas dentro de apps legítimos coletam identificadores e localização.",
         sinais=["apps gratuitos com muitas permissões"],
         defesas=["apagar o ID de publicidade", "revisar a seção de Segurança dos dados na loja"],
         refs=["OWASP M2", "OWASP M6"]),
    dict(id="PRIV-04", fam="PRIV", nome="Área de transferência lida por outros apps", tatica="Coleta",
         como="Apps leem o que você copiou (senhas, chaves de carteira).",
         sinais=["aviso 'app colou da área de transferência' (Android 12+)"],
         defesas=["não copiar senhas; usar gerenciador com preenchimento automático"],
         refs=[]),
    dict(id="PRIV-05", fam="PRIV", nome="Câmera e microfone acessados às escondidas", tatica="Coleta",
         como="App em segundo plano liga sensores.",
         sinais=["ponto verde de câmera/microfone sem uso seu"],
         defesas=["bloqueio rápido de câmera e microfone (Android 12+)", "revogar a permissão"],
         refs=[]),
    # ---------------------------------------------------------------- CONTA
    dict(id="CONTA-01", fam="CONTA", nome="Tomada da conta Google", tatica="Acesso a Credenciais",
         como="Com a conta, o atacante localiza, apaga e lê backups do aparelho.",
         sinais=["alertas de login novo", "aparelhos desconhecidos na conta"],
         defesas=["chave de acesso (passkey) ou 2FA forte", "Verificação de segurança do Google", "remover aparelhos desconhecidos"],
         refs=[]),
    dict(id="CONTA-02", fam="CONTA", nome="Sequestro de WhatsApp e mensageiros", tatica="Acesso a Credenciais",
         como="Golpista pede o código de verificação e registra a sua conta em outro aparelho.",
         sinais=["pedido de código de 6 dígitos por terceiros"],
         defesas=["confirmação em duas etapas (PIN) no mensageiro", "nunca repassar código"],
         refs=[]),
    dict(id="CONTA-03", fam="CONTA", nome="Reutilização de senha e vazamentos", tatica="Acesso a Credenciais",
         como="Senha vazada em um site é testada em todos os outros.",
         sinais=["alerta de senha comprometida do gerenciador"],
         defesas=["gerenciador de senhas", "uma senha por site", "Verificação de senhas do Google"],
         refs=[]),
    dict(id="CONTA-04", fam="CONTA", nome="Backup na nuvem acessado por terceiros", tatica="Exfiltração",
         como="Com a conta, o backup de mensagens e fotos é baixado.",
         sinais=["(conta)"],
         defesas=["backup cifrado de ponta a ponta quando o app oferece", "proteger a conta (CONTA-01)"],
         refs=[]),
    # ---------------------------------------------------------------- APP (OWASP Mobile Top 10 2024)
    dict(id="APP-M1", fam="APP", nome="M1 Uso impróprio de credenciais", tatica="Acesso a Credenciais",
         como="Chaves de API e senhas embutidas no app ou guardadas sem proteção.", sinais=["(desenvolvimento)"],
         defesas=["sem segredos no APK", "Android Keystore", "tokens de curta duração"], refs=["OWASP M1 (2024)"]),
    dict(id="APP-M2", fam="APP", nome="M2 Cadeia de suprimentos inadequada", tatica="Acesso Inicial",
         como="Bibliotecas e SDKs de terceiros comprometidos ou vulneráveis.", sinais=["(desenvolvimento)"],
         defesas=["inventário de dependências (SBOM)", "fixar versões e conferir assinaturas"], refs=["OWASP M2 (2024)"]),
    dict(id="APP-M3", fam="APP", nome="M3 Autenticação e autorização inseguras", tatica="Acesso a Credenciais",
         como="Decisões de acesso feitas só no cliente.", sinais=["(desenvolvimento)"],
         defesas=["autorizar no servidor", "biometria ligada a chave criptográfica"], refs=["OWASP M3 (2024)"]),
    dict(id="APP-M4", fam="APP", nome="M4 Validação insuficiente de entrada e saída", tatica="Execução",
         como="Injeção por intents, deep links, WebView e dados do servidor.", sinais=["(desenvolvimento)"],
         defesas=["validar todo dado externo", "WebView sem JavaScript bridge exposto"], refs=["OWASP M4 (2024)"]),
    dict(id="APP-M5", fam="APP", nome="M5 Comunicação insegura", tatica="Coleta",
         como="HTTP sem TLS, validação de certificado desligada.", sinais=["(desenvolvimento)"],
         defesas=["TLS sempre", "Network Security Config sem cleartext", "pinning onde fizer sentido"], refs=["OWASP M5 (2024)"]),
    dict(id="APP-M6", fam="APP", nome="M6 Controles de privacidade inadequados", tatica="Coleta",
         como="Coleta além do necessário, logs com dados pessoais.", sinais=["(desenvolvimento)"],
         defesas=["minimização de dados", "nada pessoal em logs"], refs=["OWASP M6 (2024)"]),
    dict(id="APP-M7", fam="APP", nome="M7 Proteção binária insuficiente", tatica="Evasão de Defesa",
         como="App fácil de reempacotar e adulterar.", sinais=["(desenvolvimento)"],
         defesas=["Play Integrity API", "ofuscação (R8)", "verificação de assinatura no servidor"], refs=["OWASP M7 (2024)"]),
    dict(id="APP-M8", fam="APP", nome="M8 Configuração de segurança incorreta", tatica="Evasão de Defesa",
         como="Componentes exportados, allowBackup, debuggable em produção.", sinais=["(desenvolvimento)"],
         defesas=["exported=false por padrão", "debuggable=false", "permissões de assinatura em componentes"], refs=["OWASP M8 (2024)"]),
    dict(id="APP-M9", fam="APP", nome="M9 Armazenamento de dados inseguro", tatica="Coleta",
         como="Dados sensíveis em armazenamento externo ou sem cifra.", sinais=["(desenvolvimento)"],
         defesas=["armazenamento interno", "EncryptedFile / Keystore"], refs=["OWASP M9 (2024)"]),
    dict(id="APP-M10", fam="APP", nome="M10 Criptografia insuficiente", tatica="Acesso a Credenciais",
         como="Algoritmos fracos, chaves fixas, modos inseguros.", sinais=["(desenvolvimento)"],
         defesas=["AES-GCM com chaves do Keystore", "nunca criptografia caseira"], refs=["OWASP M10 (2024)"]),
    # ---------------------------------------------------------------- SUP
    dict(id="SUP-01", fam="SUP", nome="Malware pré-instalado de fábrica", tatica="Persistência",
         como="Firmware de aparelhos e TV boxes baratos já vem com backdoor.",
         sinais=["apps de sistema desconhecidos que não podem ser removidos"],
         defesas=["comprar aparelhos certificados pelo Play Protect", "desativar apps de sistema suspeitos"],
         refs=["OWASP M2"]),
    dict(id="SUP-02", fam="SUP", nome="Atualização maliciosa de app legítimo", tatica="Execução",
         como="App confiável é vendido ou comprometido e recebe uma atualização maliciosa.",
         sinais=["app antigo passa a pedir permissões novas"],
         defesas=["desconfiar de pedidos novos de permissão depois de uma atualização", "remover apps abandonados"],
         refs=["OWASP M2"]),
    # ---------------------------------------------------------------- DADO
    dict(id="DADO-01", fam="DADO", nome="Arquivos sensíveis no armazenamento compartilhado", tatica="Coleta",
         como="Documentos e fotos em pastas que qualquer app com acesso a arquivos lê.",
         sinais=["apps com 'Acesso a todos os arquivos'"],
         defesas=["revogar 'Gerenciar todos os arquivos'", "usar a pasta segura (Espaço privado no Android 15+)"],
         refs=[]),
    dict(id="DADO-02", fam="DADO", nome="Dados restantes em aparelho vendido ou descartado", tatica="Exfiltração",
         como="Contas e arquivos ficam no aparelho que muda de dono.",
         sinais=["(descarte)"],
         defesas=["remover a conta Google antes", "restauração de fábrica com criptografia ligada"],
         refs=[]),
]

DEFESAS_GERAIS = [
    "Manter o Android e as atualizações do Google Play sempre em dia (o maior redutor de risco isolado).",
    "Instalar apps só da Play Store ou da loja oficial do fabricante; nunca por link de mensagem.",
    "Play Protect ligado, inclusive a verificação de apps instalados por USB.",
    "Bloqueio de tela com PIN de 6+ dígitos ou senha; biometria como conveniência, não como única barreira.",
    "Revisar mensalmente: Acessibilidade, Administradores do dispositivo, Acesso a notificações, Sobreposição, Instalar apps desconhecidos.",
    "Permissões no mínimo: 'só durante o uso' para localização, câmera e microfone; revogar SMS e registro de chamadas de quem não precisa.",
    "Chaves de acesso (passkeys) ou app autenticador no lugar de SMS; PIN no chip; confirmação em duas etapas nos mensageiros.",
    "Encontre Meu Dispositivo e proteções contra roubo ligados.",
    "DNS particular (DNS sobre TLS) e cuidado com Wi-Fi público; nenhum certificado de usuário desconhecido.",
    "Depuração USB e Opções do desenvolvedor desligadas quando não estão em uso.",
    "Bootloader bloqueado e sem root, salvo necessidade real.",
    "Backups regulares e cifrados, fora do aparelho.",
    "Para pessoas em risco elevado: Modo de Proteção Avançada (Android 16+) e chave de segurança física na conta.",
    "Em caso de comprometimento grave: trocar senhas de OUTRO aparelho, depois restauração de fábrica, depois reinstalar só o necessário.",
]

AMEACA_POR_ID = {a["id"]: a for a in AMEACAS}


def catalogo_texto():
    linhas = [f"SENTINELA {VERSAO} — catálogo: {len(AMEACAS)} ameaças em {len(FAMILIAS)} famílias", ""]
    for fam, nome in FAMILIAS.items():
        itens = [a for a in AMEACAS if a["fam"] == fam]
        linhas.append(f"== {fam}: {nome} ({len(itens)}) ==")
        for a in itens:
            linhas.append(f"[{a['id']}] {a['nome']}  (tática: {a['tatica']})")
            linhas.append(f"    como: {a['como']}")
            linhas.append(f"    sinais: {'; '.join(a['sinais'])}")
            linhas.append(f"    defesas: {'; '.join(a['defesas'])}")
            if a["refs"]:
                linhas.append(f"    refs: {'; '.join(a['refs'])}")
        linhas.append("")
    linhas.append("== Defesas gerais ==")
    linhas += [f"{i}. {d}" for i, d in enumerate(DEFESAS_GERAIS, 1)]
    return "\n".join(linhas)


def catalogo_markdown():
    m = [f"# SENTINELA {VERSAO}: ameaças ao Android e defesas", "",
         f"{len(AMEACAS)} ameaças em {len(FAMILIAS)} famílias, organizadas pelas táticas do MITRE ATT&CK Mobile; as falhas de app seguem o OWASP "
         "Mobile Top 10 (2024). Gerado por `sentinela.py --gerar-md` a partir do catálogo do código (uma fonte só).", "",
         "Nenhuma lista é completa: ameaças novas aparecem todo mês. O catálogo cobre as famílias conhecidas e os meios de defesa de cada uma.", ""]
    for fam, nome in FAMILIAS.items():
        m += [f"## {fam}: {nome}", ""]
        for a in (x for x in AMEACAS if x["fam"] == fam):
            m += [f"### {a['id']}: {a['nome']}", "", f"- **Tática:** {a['tatica']}", f"- **Como acontece:** {a['como']}",
                  "- **Sinais:** " + "; ".join(a["sinais"]), "- **Defesas:**"]
            m += [f"  - {d}" for d in a["defesas"]]
            if a["refs"]:
                m.append("- **Referências:** " + "; ".join(a["refs"]))
            m.append("")
    m += ["## Defesas gerais", ""] + [f"{i}. {d}" for i, d in enumerate(DEFESAS_GERAIS, 1)] + [""]
    m += ["## Fontes", "", "- MITRE ATT&CK Mobile: https://attack.mitre.org/matrices/mobile/",
          "- OWASP Mobile Top 10 (2024): https://owasp.org/www-project-mobile-top-10/",
          "- Indicadores de stalkerware (Echap): https://github.com/AssoEchap/stalkerware-indicators", ""]
    return "\n".join(m)


# ======================================================================================================================
# 2. EXECUTORES (só leitura, lista fechada)
# ======================================================================================================================
COMANDOS = {
    "props": "getprop",
    "pacotes3": "pm list packages -3 -i",
    "dumpsys_pacotes": "dumpsys package packages",
    "acessibilidade": "settings get secure enabled_accessibility_services",
    "notificacoes": "settings get secure enabled_notification_listeners",
    "teclado": "settings get secure default_input_method",
    "admins": "dumpsys device_policy",
    "adb": "settings get global adb_enabled",
    "dev": "settings get global development_settings_enabled",
    "verificador": "settings get global package_verifier_enable",
    "proxy": "settings get global http_proxy",
    "dns": "settings get global private_dns_mode",
    "fontes_legado": "settings get secure install_non_market_apps",
    "bloqueio": "locksettings get-disabled",
    "su": "which su",
    "instalar_desconhecidos": "cmd appops query-op --user 0 REQUEST_INSTALL_PACKAGES allow",
    "sobreposicao": "cmd appops query-op --user 0 SYSTEM_ALERT_WINDOW allow",
}


class ExecutorRecusou(Exception):
    pass


class ExecutorAdb:
    """Roda `adb shell <comando>` só para os comandos da lista fechada COMANDOS (todos de leitura)."""

    def __init__(self, serial=None, timeout=60):
        self.adb = shutil.which("adb")
        if not self.adb:
            raise SystemExit("adb não encontrado no PATH. Instale as Android Platform Tools e autorize a depuração USB no aparelho.")
        self.serial, self.timeout = serial, timeout

    def __call__(self, chave):
        if chave not in COMANDOS:
            raise ExecutorRecusou(chave)
        cmd = [self.adb] + (["-s", self.serial] if self.serial else []) + ["shell"] + COMANDOS[chave].split()
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
        except subprocess.TimeoutExpired:
            return None
        return r.stdout if r.returncode == 0 else (r.stdout or None)


class ExecutorGravado:
    """Responde a partir de um dicionário {chave: saída} (captura salva ou aparelho simulado). Também recusa chaves fora da lista."""

    def __init__(self, saidas):
        self.saidas = saidas

    def __call__(self, chave):
        if chave not in COMANDOS:
            raise ExecutorRecusou(chave)
        return self.saidas.get(chave)


def capturar(executor):
    return {"sentinela": VERSAO, "capturado_em": datetime.datetime.now().isoformat(timespec="seconds"),
            "saidas": {k: executor(k) for k in COMANDOS}}


# ======================================================================================================================
# 3. LEITORES DAS SAÍDAS
# ======================================================================================================================
def ler_props(texto):
    return dict(re.findall(r"^\[([^\]]+)\]: \[([^\]]*)\]", texto or "", re.M))


def ler_pacotes(texto):
    """'package:com.x  installer=com.android.vending' -> {pacote: instalador ou None}."""
    saida = {}
    for linha in (texto or "").splitlines():
        m = re.match(r"\s*package:(\S+)(?:\s+installer=(\S+))?", linha)
        if m:
            inst = m.group(2)
            saida[m.group(1)] = None if inst in (None, "null") else inst
    return saida


def ler_componentes(texto):
    """'com.a/.Svc:com.b/com.b.X' -> {'com.a', 'com.b'}; 'null' ou vazio -> conjunto vazio."""
    texto = (texto or "").strip()
    if not texto or texto == "null":
        return set()
    return {c.split("/")[0] for c in texto.split(":") if "/" in c}


def ler_admins(texto):
    return set(re.findall(r"ComponentInfo\{([^/}]+)/", texto or ""))


def ler_permissoes(texto):
    """dumpsys package packages -> {pacote: conjunto de permissões concedidas}."""
    perms, atual = {}, None
    for linha in (texto or "").splitlines():
        m = re.match(r"\s*Package \[([^\]]+)\]", linha)
        if m:
            atual = m.group(1)
            perms.setdefault(atual, set())
            continue
        m = re.match(r"\s*([\w.]+): granted=true", linha)
        if m and atual:
            perms[atual].add(m.group(1))
    return perms


def ler_lista_pacotes(texto):
    """Saída de 'appops query-op': um pacote por linha."""
    return {l.strip() for l in (texto or "").splitlines() if re.fullmatch(r"[A-Za-z][\w.]*", l.strip() or "-")}


def ler_ioc(caminho):
    """Lista de pacotes: texto simples (um pacote por linha) ou o ioc.yaml do Echap (só os itens das listas 'packages:')."""
    pacotes, yaml, em_pacotes = set(), False, False
    nome_pacote = re.compile(r"[a-zA-Z][\w]*(\.[\w]+)+")
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            l = linha.strip()
            if not l or l.startswith("#"):
                continue
            chave = re.match(r"(?:- )?([A-Za-z_]+):", l)
            if chave:
                yaml = True
                em_pacotes = chave.group(1) == "packages"
                continue
            if l.startswith("- "):
                l = l[2:].strip()
            elif yaml:
                continue
            l = l.strip("'\"")
            if (em_pacotes or not yaml) and nome_pacote.fullmatch(l):
                pacotes.add(l)
    return pacotes


# ======================================================================================================================
# 4. A CONTA: razões de verossimilhança e decisão em três níveis
# ======================================================================================================================
# P(sinal | app malicioso) / P(sinal | app benigno), valores de PARTIDA (especialista), não medidos. O log das razões soma, com teto
# (os sinais são correlacionados: o Naive Bayes conta duas vezes a mesma evidência, Parte 34 da SYNTHAI).
RAZOES = {
    "fora_da_loja": (3.0, "instalado fora de loja oficial", "ABU-07"),
    "acessibilidade": (8.0, "serviço de Acessibilidade ativo", "ABU-01"),
    "admin": (5.0, "Administrador do dispositivo", "ABU-02"),
    "notificacoes": (3.0, "lê todas as notificações", "ABU-03"),
    "sobreposicao": (2.0, "pode sobrepor outros apps", "ABU-04"),
    "instala_apps": (2.5, "pode instalar outros apps", "MAL-06"),
    "sms": (3.0, "lê ou envia SMS", "MAL-04"),
    "chamadas": (2.0, "registro de chamadas", "ABU-08"),
    "vigilancia": (3.0, "microfone + câmera + localização juntos", "MAL-02"),
    "localizacao_fundo": (1.8, "localização em segundo plano", "PRIV-01"),
    "todos_arquivos": (1.5, "acesso a todos os arquivos", "DADO-01"),
    "teclado": (2.0, "é o teclado padrão", "ABU-05"),
    "ioc": (1000.0, "consta da lista de indicadores (--ioc)", "MAL-02"),
}
PRIORI = 0.02          # fração de apps de terceiros maliciosos antes de olhar os sinais (partida conservadora)
TETO_LOG_RV = math.log(200.0)  # teto do total sem IOC
LIMIAR_REVISAR, LIMIAR_ALTO = 0.10, 0.60

LOJAS = {"com.android.vending", "com.sec.android.app.samsungapps", "com.huawei.appmarket", "com.amazon.venezia",
         "com.xiaomi.market", "com.heytap.market", "com.oppo.market", "com.vivo.appstore", "org.fdroid.fdroid",
         "com.google.android.packageinstaller.ota"}
TECLADOS_CONHECIDOS = {"com.google.android.inputmethod.latin", "com.samsung.android.honeyboard", "com.touchtype.swiftkey",
                       "com.android.inputmethod.latin"}
ROOT_APPS = {"com.topjohnwu.magisk", "eu.chainfire.supersu", "me.weishu.kernelsu"}


def sinais_do_app(pkg, instalador, perms, acess, notif, admins, sobrep, instala, teclado, ioc):
    s = []
    if instalador not in LOJAS:
        s.append("fora_da_loja")
    if pkg in acess:
        s.append("acessibilidade")
    if pkg in admins:
        s.append("admin")
    if pkg in notif:
        s.append("notificacoes")
    if pkg in sobrep or "android.permission.SYSTEM_ALERT_WINDOW" in perms:
        s.append("sobreposicao")
    if pkg in instala:
        s.append("instala_apps")
    if perms & {"android.permission.READ_SMS", "android.permission.RECEIVE_SMS", "android.permission.SEND_SMS"}:
        s.append("sms")
    if perms & {"android.permission.READ_CALL_LOG", "android.permission.PROCESS_OUTGOING_CALLS"}:
        s.append("chamadas")
    if {"android.permission.RECORD_AUDIO", "android.permission.CAMERA", "android.permission.ACCESS_FINE_LOCATION"} <= perms:
        s.append("vigilancia")
    if "android.permission.ACCESS_BACKGROUND_LOCATION" in perms:
        s.append("localizacao_fundo")
    if "android.permission.MANAGE_EXTERNAL_STORAGE" in perms:
        s.append("todos_arquivos")
    if pkg == teclado and pkg not in TECLADOS_CONHECIDOS:
        s.append("teclado")
    if pkg in ioc:
        s.append("ioc")
    return s


def posterior(sinais, priori=PRIORI):
    """P(malicioso | sinais) por razões de verossimilhança, com teto no total quando não há IOC."""
    log_rv = sum(math.log(RAZOES[x][0]) for x in sinais if x != "ioc")
    log_rv = min(log_rv, TETO_LOG_RV)
    if "ioc" in sinais:
        log_rv += math.log(RAZOES["ioc"][0])
    chance = priori / (1 - priori) * math.exp(log_rv)
    return chance / (1 + chance)


def decidir(p):
    """Três níveis: a faixa do meio devolve a decisão a você (perguntar custa menos que errar)."""
    if p >= LIMIAR_ALTO:
        return "ALTO RISCO"
    if p >= LIMIAR_REVISAR:
        return "REVISAR"
    return "OK"


# ======================================================================================================================
# 5. A AUDITORIA
# ======================================================================================================================
def _achado(nivel, titulo, ameaca, detalhe=""):
    return {"nivel": nivel, "titulo": titulo, "ameaca": ameaca, "detalhe": detalhe,
            "defesas": AMEACA_POR_ID[ameaca]["defesas"]}


def auditar(executor, ioc=frozenset(), hoje=None):
    hoje = hoje or datetime.date.today()
    props = ler_props(executor("props"))
    pacotes = ler_pacotes(executor("pacotes3"))
    perms = ler_permissoes(executor("dumpsys_pacotes"))
    acess = ler_componentes(executor("acessibilidade"))
    notif = ler_componentes(executor("notificacoes"))
    teclado_txt = (executor("teclado") or "").strip()
    teclado = teclado_txt.split("/")[0] if "/" in teclado_txt else None
    admins = ler_admins(executor("admins"))
    sobrep = ler_lista_pacotes(executor("sobreposicao"))
    instala = ler_lista_pacotes(executor("instalar_desconhecidos"))
    achados, nao_verificado = [], []

    def valor(chave):
        v = executor(chave)
        if v is None:
            nao_verificado.append(COMANDOS[chave])
            return None
        return v.strip()

    # ---- sistema
    patch = props.get("ro.build.version.security_patch")
    if patch:
        try:
            dias = (hoje - datetime.date.fromisoformat(patch)).days
            if dias > 365:
                achados.append(_achado("ALTO", f"Patch de segurança de {patch} ({dias} dias)", "SIS-02",
                                       "mais de um ano sem correções: o aparelho pode estar fora de suporte"))
            elif dias > 90:
                achados.append(_achado("MÉDIO", f"Patch de segurança de {patch} ({dias} dias)", "SIS-01"))
        except ValueError:
            nao_verificado.append("data do patch")
    else:
        nao_verificado.append("ro.build.version.security_patch")
    if props.get("ro.boot.verifiedbootstate") in ("orange", "yellow", "red") or props.get("ro.boot.flash.locked") == "0" \
            or props.get("ro.boot.vbmeta.device_state") == "unlocked":
        achados.append(_achado("ALTO", "Bootloader desbloqueado ou boot não verificado", "SIS-03",
                               f"verifiedbootstate={props.get('ro.boot.verifiedbootstate')}, flash.locked={props.get('ro.boot.flash.locked')}"))
    if "test-keys" in props.get("ro.build.tags", "") or props.get("ro.debuggable") == "1" or props.get("ro.secure") == "0":
        achados.append(_achado("ALTO", "Firmware com chaves de teste ou depurável", "SIS-05",
                               f"tags={props.get('ro.build.tags')}, debuggable={props.get('ro.debuggable')}"))
    if props.get("ro.crypto.state") and props.get("ro.crypto.state") != "encrypted":
        achados.append(_achado("ALTO", "Armazenamento sem criptografia", "SIS-06", f"ro.crypto.state={props.get('ro.crypto.state')}"))
    su = valor("su")
    raiz = sorted(ROOT_APPS & set(pacotes))
    if su or raiz:
        achados.append(_achado("ALTO", "Root detectado", "SIS-04", f"su={su or '-'}; apps={', '.join(raiz) or '-'}"))
    if valor("verificador") == "0":
        achados.append(_achado("ALTO", "Play Protect (verificação de apps) desligado", "SIS-07"))
    # ---- acesso físico
    if valor("adb") == "1":
        achados.append(_achado("INFO", "Depuração USB ligada (esperado durante esta auditoria)", "FIS-03",
                               "desligue ao terminar"))
    if valor("dev") == "1":
        achados.append(_achado("BAIXO", "Opções do desenvolvedor ligadas", "FIS-03"))
    bloqueio = valor("bloqueio")
    if bloqueio == "true":
        achados.append(_achado("ALTO", "Sem bloqueio de tela", "FIS-02"))
    # ---- rede
    proxy = valor("proxy")
    if proxy and proxy not in ("null", ":0"):
        achados.append(_achado("ALTO", f"Proxy HTTP global: {proxy}", "REDE-03"))
    dns = valor("dns")
    if dns in ("off",):
        achados.append(_achado("BAIXO", "DNS particular desligado", "REDE-04"))
    if valor("fontes_legado") == "1":
        achados.append(_achado("MÉDIO", "Fontes desconhecidas liberadas para todo o sistema (Android antigo)", "ABU-07"))
    # ---- componentes de terceiros com poderes especiais (inclusive apps que não estão na lista -3)
    for nome, conj, amea in (("Acessibilidade", acess, "ABU-01"), ("Acesso a notificações", notif, "ABU-03"),
                             ("Administrador do dispositivo", admins, "ABU-02")):
        for pkg in sorted(conj):
            if pkg in pacotes:
                achados.append(_achado("MÉDIO", f"{nome}: {pkg}", amea, "app de terceiros com este poder: confirme que você reconhece"))
    # ---- apps de terceiros: conta e decisão
    apps = []
    for pkg, inst in sorted(pacotes.items()):
        s = sinais_do_app(pkg, inst, perms.get(pkg, set()), acess, notif, admins, sobrep, instala, teclado, ioc)
        p = posterior(s)
        apps.append({"pacote": pkg, "instalador": inst, "sinais": s, "p": p, "decisao": decidir(p),
                     "motivos": [RAZOES[x][1] for x in s], "ameacas": sorted({RAZOES[x][2] for x in s})})
    apps.sort(key=lambda a: -a["p"])
    ordem = {"ALTO": 0, "MÉDIO": 1, "BAIXO": 2, "INFO": 3}
    achados.sort(key=lambda a: ordem[a["nivel"]])
    return {"sentinela": VERSAO, "data": hoje.isoformat(), "modelo": props.get("ro.product.model"),
            "android": props.get("ro.build.version.release"), "patch": patch, "achados": achados, "apps": apps,
            "nao_verificado": nao_verificado, "ioc_carregados": len(ioc)}


def relatorio_texto(r):
    linhas = [f"SENTINELA {r['sentinela']}: relatório de {r['data']}",
              f"Aparelho: {r['modelo'] or '?'}, Android {r['android'] or '?'}, patch {r['patch'] or '?'}", ""]
    contagem = {}
    for a in r["apps"]:
        contagem[a["decisao"]] = contagem.get(a["decisao"], 0) + 1
    linhas.append(f"Achados do aparelho: {len(r['achados'])}. Apps de terceiros: {len(r['apps'])} "
                  f"(ALTO RISCO {contagem.get('ALTO RISCO', 0)}, REVISAR {contagem.get('REVISAR', 0)}, OK {contagem.get('OK', 0)}).")
    linhas.append("")
    linhas.append("== Aparelho ==")
    for a in r["achados"] or []:
        amea = AMEACA_POR_ID[a["ameaca"]]
        linhas.append(f"[{a['nivel']}] {a['titulo']}  -> {a['ameaca']} {amea['nome']}")
        if a["detalhe"]:
            linhas.append(f"    {a['detalhe']}")
        linhas.append(f"    o que fazer: {a['defesas'][0]}")
    if not r["achados"]:
        linhas.append("nenhum achado")
    linhas.append("")
    linhas.append("== Apps de terceiros (do mais suspeito ao menos) ==")
    for a in r["apps"]:
        if a["decisao"] == "OK":
            continue
        linhas.append(f"[{a['decisao']}] {a['pacote']}  (p ≈ {a['p']:.2f}; instalador: {a['instalador'] or 'desconhecido'})")
        linhas.append(f"    sinais: {'; '.join(a['motivos'])}")
        for amid in a["ameacas"]:
            linhas.append(f"    {amid} {AMEACA_POR_ID[amid]['nome']}: {AMEACA_POR_ID[amid]['defesas'][0]}")
    ok = sum(1 for a in r["apps"] if a["decisao"] == "OK")
    linhas.append(f"({ok} apps sem sinais relevantes não listados)")
    if r["nao_verificado"]:
        linhas.append("")
        linhas.append("Não verificado (o aparelho não respondeu ou a versão não tem o comando): " + "; ".join(r["nao_verificado"]))
    linhas += ["", "Lembretes: a probabilidade é uma ordem de grandeza (razões de partida, não medidas); 'REVISAR' quer dizer que a decisão é sua;",
               f"sem --ioc (carregados agora: {r['ioc_carregados']}) a SENTINELA não reconhece malware pelo nome; uma varredura limpa não prova ausência.",
               "Ao terminar, desligue a depuração USB."]
    return "\n".join(linhas)


def relatorio_markdown(r):
    return "# Relatório SENTINELA\n\n```\n" + relatorio_texto(r) + "\n```\n"


# ======================================================================================================================
# 6. APARELHO SIMULADO (demonstração e testes)
# ======================================================================================================================
def aparelho_simulado():
    return {
        "props": "[ro.product.model]: [Simulado X1]\n[ro.build.version.release]: [11]\n[ro.build.version.security_patch]: [2024-03-05]\n"
                 "[ro.boot.verifiedbootstate]: [green]\n[ro.boot.flash.locked]: [1]\n[ro.build.tags]: [release-keys]\n"
                 "[ro.debuggable]: [0]\n[ro.secure]: [1]\n[ro.crypto.state]: [encrypted]\n",
        "pacotes3": "package:com.exemplo.lanterna  installer=null\npackage:com.exemplo.banco  installer=com.android.vending\n"
                    "package:com.exemplo.servico  installer=com.google.android.packageinstaller\n"
                    "package:com.exemplo.jogo  installer=com.android.vending\n",
        "dumpsys_pacotes": "Packages:\n  Package [com.exemplo.lanterna] (abc):\n    install permissions:\n"
                           "      android.permission.SYSTEM_ALERT_WINDOW: granted=true\n    runtime permissions:\n"
                           "      android.permission.READ_SMS: granted=true\n      android.permission.CAMERA: granted=false\n"
                           "  Package [com.exemplo.banco] (def):\n    runtime permissions:\n      android.permission.CAMERA: granted=true\n"
                           "  Package [com.exemplo.servico] (ghi):\n    runtime permissions:\n      android.permission.RECORD_AUDIO: granted=true\n"
                           "      android.permission.CAMERA: granted=true\n      android.permission.ACCESS_FINE_LOCATION: granted=true\n"
                           "      android.permission.ACCESS_BACKGROUND_LOCATION: granted=true\n      android.permission.READ_CALL_LOG: granted=true\n"
                           "  Package [com.exemplo.jogo] (jkl):\n    runtime permissions:\n",
        "acessibilidade": "com.exemplo.servico/com.exemplo.servico.Acess",
        "notificacoes": "com.exemplo.servico/.Notif:com.google.android.gms/.Wear",
        "teclado": "com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME",
        "admins": "Device Policy Manager:\n  Enabled Device Admins (User 0):\n    admin=ComponentInfo{com.exemplo.servico/com.exemplo.servico.Admin}\n",
        "adb": "1", "dev": "1", "verificador": "1", "proxy": "10.0.0.5:8080", "dns": "off", "fontes_legado": "null",
        "bloqueio": "false", "su": "",
        "instalar_desconhecidos": "com.exemplo.lanterna\n",
        "sobreposicao": "com.exemplo.lanterna\n",
    }


# ======================================================================================================================
# 7. TESTES
# ======================================================================================================================
class Testes(unittest.TestCase):
    def test_catalogo_ids_unicos_e_completos(self):
        ids = [a["id"] for a in AMEACAS]
        self.assertEqual(len(ids), len(set(ids)))
        for a in AMEACAS:
            self.assertIn(a["fam"], FAMILIAS)
            self.assertTrue(a["defesas"] and a["sinais"] and a["como"])
        self.assertEqual({a["fam"] for a in AMEACAS}, set(FAMILIAS))

    def test_toda_razao_aponta_para_ameaca_existente(self):
        for rv, _, amea in RAZOES.values():
            self.assertIn(amea, AMEACA_POR_ID)
            self.assertGreater(rv, 1.0)

    def test_executor_recusa_comando_fora_da_lista(self):
        ex = ExecutorGravado({})
        with self.assertRaises(ExecutorRecusou):
            ex("rm -rf /sdcard")

    def test_comandos_sao_de_leitura(self):
        for c in COMANDOS.values():
            self.assertFalse(re.search(r"\b(rm|install|uninstall|put|disable|kill|reboot|wipe)\b", c), c)

    def test_ler_pacotes(self):
        r = ler_pacotes("package:com.a  installer=com.android.vending\npackage:com.b installer=null\npackage:com.c\n")
        self.assertEqual(r, {"com.a": "com.android.vending", "com.b": None, "com.c": None})

    def test_ler_componentes(self):
        self.assertEqual(ler_componentes("com.a/.S:com.b/com.b.X"), {"com.a", "com.b"})
        self.assertEqual(ler_componentes("null"), set())
        self.assertEqual(ler_componentes(None), set())

    def test_ler_permissoes_so_concedidas(self):
        r = ler_permissoes(aparelho_simulado()["dumpsys_pacotes"])
        self.assertIn("android.permission.READ_SMS", r["com.exemplo.lanterna"])
        self.assertNotIn("android.permission.CAMERA", r["com.exemplo.lanterna"])
        self.assertEqual(r["com.exemplo.jogo"], set())

    def test_posterior_forma_fechada(self):
        # um sinal de razão 8 com priori 0,02: chance 0,02/0,98·8 = 0,16327 -> p = 0,14035
        self.assertAlmostEqual(posterior(["acessibilidade"]), (0.02 / 0.98 * 8) / (1 + 0.02 / 0.98 * 8), places=12)
        self.assertAlmostEqual(posterior([]), 0.02, places=12)

    def test_teto_sem_ioc_e_ioc_decide(self):
        todos = [k for k in RAZOES if k != "ioc"]
        teto = (0.02 / 0.98 * 200) / (1 + 0.02 / 0.98 * 200)
        self.assertAlmostEqual(posterior(todos), teto, places=12)
        self.assertEqual(decidir(posterior(["ioc"])), "ALTO RISCO")

    def test_decisao_em_tres_niveis(self):
        self.assertEqual(decidir(0.05), "OK")
        self.assertEqual(decidir(0.3), "REVISAR")
        self.assertEqual(decidir(0.9), "ALTO RISCO")

    def test_auditoria_simulada(self):
        r = auditar(ExecutorGravado(aparelho_simulado()), hoje=datetime.date(2026, 11, 1))
        titulos = " | ".join(a["titulo"] for a in r["achados"])
        self.assertIn("Patch de segurança de 2024-03-05", titulos)
        self.assertIn("Proxy HTTP global", titulos)
        por = {a["pacote"]: a for a in r["apps"]}
        self.assertEqual(por["com.exemplo.servico"]["decisao"], "ALTO RISCO")
        self.assertIn(por["com.exemplo.lanterna"]["decisao"], ("REVISAR", "ALTO RISCO"))
        self.assertEqual(por["com.exemplo.banco"]["decisao"], "OK")
        self.assertEqual(r["apps"][0]["pacote"], "com.exemplo.servico")

    def test_aparelho_limpo_sem_achados_altos(self):
        s = aparelho_simulado()
        s.update(props=s["props"].replace("2024-03-05", "2026-10-01"), proxy="null", dns="hostname", acessibilidade="null",
                 notificacoes="null", admins="", instalar_desconhecidos="", sobreposicao="", adb="0", dev="0",
                 pacotes3="package:com.exemplo.banco  installer=com.android.vending\n")
        r = auditar(ExecutorGravado(s), hoje=datetime.date(2026, 11, 1))
        self.assertFalse([a for a in r["achados"] if a["nivel"] in ("ALTO", "MÉDIO")])
        self.assertEqual([a["decisao"] for a in r["apps"]], ["OK"])

    def test_comando_ausente_vira_nao_verificado(self):
        s = aparelho_simulado()
        del s["bloqueio"]
        r = auditar(ExecutorGravado(s), hoje=datetime.date(2026, 11, 1))
        self.assertIn(COMANDOS["bloqueio"], r["nao_verificado"])

    def test_ioc_texto_e_yaml(self):
        import os
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as f:
            f.write("- name: X\n  packages:\n  - com.exemplo.servico\n  - 'com.outro.app'\n  websites:\n  - exemplo.com\n# com.comentario.app\n")
        try:
            self.assertEqual(ler_ioc(f.name), {"com.exemplo.servico", "com.outro.app"})
        finally:
            os.unlink(f.name)
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("com.a.b\n# com.c.d\ncom.e.f\n")
        try:
            self.assertEqual(ler_ioc(f.name), {"com.a.b", "com.e.f"})
        finally:
            os.unlink(f.name)

    def test_markdown_tem_todas_as_ameacas(self):
        md = catalogo_markdown()
        for a in AMEACAS:
            self.assertIn(f"### {a['id']}:", md)


# ======================================================================================================================
# 8. LINHA DE COMANDO
# ======================================================================================================================
def main(argv=None):
    ap = argparse.ArgumentParser(description="SENTINELA: auditoria defensiva de Android (só leitura).")
    ap.add_argument("--catalogo", action="store_true")
    ap.add_argument("--gerar-md")
    ap.add_argument("--auditar", action="store_true")
    ap.add_argument("--capturar")
    ap.add_argument("--analisar")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--testes", action="store_true")
    ap.add_argument("--serial")
    ap.add_argument("--ioc")
    ap.add_argument("--json")
    ap.add_argument("--relatorio")
    a = ap.parse_args(argv)
    if a.testes:
        r = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(Testes))
        return 0 if r.wasSuccessful() else 1
    if a.catalogo:
        print(catalogo_texto())
        return 0
    if a.gerar_md:
        with open(a.gerar_md, "w", encoding="utf-8") as f:
            f.write(catalogo_markdown())
        print("catálogo escrito em", a.gerar_md)
        return 0
    if a.capturar:
        with open(a.capturar, "w", encoding="utf-8") as f:
            json.dump(capturar(ExecutorAdb(a.serial)), f, ensure_ascii=False, indent=1)
        print("captura salva em", a.capturar)
        return 0
    ioc = frozenset(ler_ioc(a.ioc)) if a.ioc else frozenset()
    if a.demo:
        executor = ExecutorGravado(aparelho_simulado())
        print("(aparelho SIMULADO, com problemas plantados)\n")
    elif a.analisar:
        with open(a.analisar, encoding="utf-8") as f:
            executor = ExecutorGravado(json.load(f)["saidas"])
    elif a.auditar:
        executor = ExecutorAdb(a.serial)
    else:
        ap.print_help()
        return 0
    r = auditar(executor, ioc=ioc)
    print(relatorio_texto(r))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=1)
    if a.relatorio:
        with open(a.relatorio, "w", encoding="utf-8") as f:
            f.write(relatorio_markdown(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
