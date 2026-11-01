# SENTINELA 1.0: ameaças ao Android e defesas

72 ameaças em 12 famílias, organizadas pelas táticas do MITRE ATT&CK Mobile; as falhas de app seguem o OWASP Mobile Top 10 (2024). Gerado por `sentinela.py --gerar-md` a partir do catálogo do código (uma fonte só).

Nenhuma lista é completa: ameaças novas aparecem todo mês. O catálogo cobre as famílias conhecidas e os meios de defesa de cada uma.

## MAL: Malware e apps maliciosos

### MAL-01: Trojan bancário com sobreposição (overlay)

- **Tática:** Acesso a Credenciais
- **Como acontece:** O app desenha uma tela falsa por cima do app do banco e captura senha e token; costuma pedir Acessibilidade para tocar sozinho.
- **Sinais:** permissão 'Sobrepor a outros apps' em app sem motivo; serviço de Acessibilidade ativo em app desconhecido; pedido insistente de Acessibilidade logo após instalar
- **Defesas:**
  - negar Acessibilidade e Sobreposição a apps que não precisam
  - instalar só da Play Store ou loja oficial
  - usar o app do banco com biometria e notificação de transação
  - Play Protect ligado
- **Referências:** MITRE: Acesso a Credenciais (captura de entrada / sobreposição)

### MAL-02: Spyware comercial e stalkerware

- **Tática:** Coleta
- **Como acontece:** App instalado por alguém com acesso ao aparelho (ou por exploit) que copia mensagens, localização, chamadas e microfone.
- **Sinais:** app sem ícone ou com nome genérico ('Serviço do sistema', 'Wi-Fi'); administrador do dispositivo desconhecido; Acessibilidade + leitor de notificações + localização em segundo plano no mesmo app; bateria e dados móveis altos sem motivo
- **Defesas:**
  - conferir Administradores do dispositivo, Acessibilidade e Acesso a notificações
  - comparar com lista de indicadores (--ioc)
  - trocar a senha da conta Google de outro aparelho
  - em caso de violência doméstica, buscar apoio antes de remover (o agressor percebe)
  - restauração de fábrica quando houver dúvida
- **Referências:** Coalition Against Stalkerware; Echap stalkerware-indicators

### MAL-03: Ransomware e bloqueio de tela

- **Tática:** Impacto
- **Como acontece:** Cifra arquivos acessíveis ou trava a tela pedindo resgate; usa Administrador do dispositivo para impedir a remoção.
- **Sinais:** administrador do dispositivo em app recém-instalado; Sobreposição permanente; acesso a todos os arquivos sem motivo
- **Defesas:**
  - backup regular fora do aparelho
  - não conceder Administrador do dispositivo
  - modo de segurança para desinstalar
  - nunca pagar resgate (não garante a devolução)
- **Referências:** MITRE: Impacto

### MAL-04: Fraude de SMS premium e assinaturas (toll fraud)

- **Tática:** Impacto
- **Como acontece:** Envia SMS pagos ou assina serviços de operadora em segundo plano, interceptando o SMS de confirmação.
- **Sinais:** permissões de enviar/ler SMS em app que não é de mensagens; cobranças desconhecidas na conta da operadora
- **Defesas:**
  - negar SMS a apps que não são o app padrão de mensagens
  - pedir bloqueio de serviços premium (VAS) à operadora
- **Referências:** MITRE: Impacto (fraude de cobrança)

### MAL-05: Adware, fraude de cliques e anúncios ocultos

- **Tática:** Impacto
- **Como acontece:** Abre anúncios fora do app, clica em anúncios em segundo plano, ou esconde o próprio ícone para não ser removido.
- **Sinais:** anúncios em tela cheia fora de qualquer app; app sem ícone no menu; Sobreposição concedida
- **Defesas:**
  - em Configurações > Apps, ordenar por uso recente e remover o desconhecido
  - Play Protect

### MAL-06: Dropper e carregador (baixa o malware depois)

- **Tática:** Execução
- **Como acontece:** App aparentemente útil passa na revisão da loja e depois baixa e instala o código malicioso.
- **Sinais:** permissão 'Instalar apps desconhecidos' em app que não é loja nem navegador; pedido de atualização fora da loja
- **Defesas:**
  - negar 'Instalar apps desconhecidos' a todos os apps (liberar só na hora, e revogar)
  - Play Protect
- **Referências:** MITRE: Execução / Download de código novo

### MAL-07: Trojan de acesso remoto (RAT)

- **Tática:** Comando e Controle
- **Como acontece:** Dá ao atacante controle do aparelho: tela, toques, câmera, arquivos; geralmente via Acessibilidade e MediaProjection.
- **Sinais:** Acessibilidade em app desconhecido; ícone de gravação/transmissão de tela aparecendo sozinho
- **Defesas:**
  - remover Acessibilidade de apps desconhecidos
  - restauração de fábrica se houver controle remoto confirmado
- **Referências:** MITRE: Comando e Controle

### MAL-08: Mineração de criptomoeda e botnet

- **Tática:** Impacto
- **Como acontece:** Usa a CPU e a rede do aparelho para minerar ou para ataques a terceiros.
- **Sinais:** aquecimento e bateria anormais; uso de dados em segundo plano alto
- **Defesas:**
  - conferir o uso de bateria e de dados por app
  - remover o app suspeito

### MAL-09: Rootkit e exploit de escalada de privilégio

- **Tática:** Escalada de Privilégio
- **Como acontece:** Explora falha do kernel ou do sistema para ganhar root e se esconder abaixo dos apps.
- **Sinais:** binário su presente sem você ter feito root; build com chaves de teste; verificação de boot fora do verde
- **Defesas:**
  - manter o patch de segurança em dia
  - restauração de fábrica e reflash da imagem oficial
- **Referências:** MITRE: Escalada de Privilégio

### MAL-10: Apps falsos e reempacotados (clones)

- **Tática:** Acesso Inicial
- **Como acontece:** Cópia de app famoso, com o mesmo nome e ícone, assinada por outro desenvolvedor e com código malicioso a mais.
- **Sinais:** app instalado fora da loja; desenvolvedor diferente do oficial; permissões a mais que o original
- **Defesas:**
  - instalar a partir do link oficial do desenvolvedor
  - conferir o nome do desenvolvedor na loja
- **Referências:** MITRE: Acesso Inicial

### MAL-11: Golpe de app de empréstimo ou investimento falso

- **Tática:** Coleta
- **Como acontece:** App financeiro falso coleta contatos e fotos para extorsão, ou mostra lucros fictícios para tomar depósitos.
- **Sinais:** app financeiro fora da loja; permissão de contatos e arquivos em app de empréstimo
- **Defesas:**
  - conferir no órgão regulador se a empresa é autorizada
  - negar contatos e fotos

## ABU: Abuso de recursos legítimos do Android

### ABU-01: Abuso de Acessibilidade

- **Tática:** Evasão de Defesa
- **Como acontece:** O serviço de Acessibilidade lê toda a tela e toca por você: é a chave-mestra dos trojans e RATs modernos.
- **Sinais:** serviço de Acessibilidade ativo de app que não é de acessibilidade, senha ou automação conhecida
- **Defesas:**
  - Configurações > Acessibilidade > Apps instalados: desligar o que não reconhece
  - Android 13+: configurações restritas para apps sideloaded
- **Referências:** MITRE: Evasão de Defesa / Coleta

### ABU-02: Abuso de Administrador do dispositivo

- **Tática:** Persistência
- **Como acontece:** Com Administrador, o app pode travar a tela, apagar dados e dificultar a desinstalação.
- **Sinais:** administrador do dispositivo que não é Encontre Meu Dispositivo nem gestão da empresa
- **Defesas:**
  - Configurações > Segurança > Apps de administração do dispositivo: desativar e depois desinstalar
- **Referências:** MITRE: Persistência

### ABU-03: Leitor de notificações (rouba códigos 2FA e mensagens)

- **Tática:** Coleta
- **Como acontece:** O acesso a notificações lê todo SMS, código de verificação e mensagem que aparece na barra.
- **Sinais:** acesso a notificações concedido a app que não é relógio, carro ou assistente conhecido
- **Defesas:**
  - Configurações > Notificações > Acesso a notificações: revogar
  - preferir app autenticador ou chave de segurança a SMS
- **Referências:** MITRE: Coleta

### ABU-04: Sobreposição e tapjacking

- **Tática:** Acesso a Credenciais
- **Como acontece:** Uma janela por cima engana o toque: você pensa que toca em 'Cancelar' e concede uma permissão.
- **Sinais:** 'Sobrepor a outros apps' concedido a app sem motivo
- **Defesas:**
  - Configurações > Apps > Acesso especial > Sobrepor a outros apps: revogar
- **Referências:** OWASP M8

### ABU-05: Teclado malicioso (keylogger)

- **Tática:** Acesso a Credenciais
- **Como acontece:** Um teclado de terceiros vê tudo o que você digita, inclusive senhas.
- **Sinais:** teclado padrão que não é o do fabricante nem o Gboard/SwiftKey
- **Defesas:**
  - usar o teclado do sistema
  - remover teclados não usados em Idiomas e entrada
- **Referências:** MITRE: Acesso a Credenciais (captura de entrada)

### ABU-06: Captura e transmissão de tela (MediaProjection)

- **Tática:** Coleta
- **Como acontece:** O app grava ou transmite a tela, incluindo senhas e mensagens.
- **Sinais:** indicador de gravação de tela aparecendo sem você pedir
- **Defesas:**
  - negar a captura quando não foi você que pediu
  - revisar os indicadores de privacidade (Android 12+)
- **Referências:** MITRE: Coleta (captura de tela)

### ABU-07: Instalação de fontes desconhecidas (sideload)

- **Tática:** Acesso Inicial
- **Como acontece:** App com 'Instalar apps desconhecidos' pode instalar outros apps sem passar pela loja.
- **Sinais:** apps com 'Instalar apps desconhecidos' permitido; apps cujo instalador não é uma loja
- **Defesas:**
  - revogar 'Instalar apps desconhecidos' de todos
  - Play Protect verificando apps instalados por USB
- **Referências:** MITRE: Acesso Inicial

### ABU-08: Excesso de permissões perigosas

- **Tática:** Coleta
- **Como acontece:** Câmera, microfone, localização em segundo plano, SMS, registro de chamadas e contatos em app que não precisa.
- **Sinais:** app com SMS, chamadas, microfone e localização juntos
- **Defesas:**
  - Painel de privacidade e Gerenciador de permissões: revogar
  - remover permissões de apps não usados (automático no Android 11+)
- **Referências:** OWASP M6

### ABU-09: Sequestro de tarefa e de intent (StrandHogg e afins)

- **Tática:** Evasão de Defesa
- **Como acontece:** App malicioso se insere na pilha de telas de um app legítimo ou intercepta intents implícitos.
- **Sinais:** tela de login aparece de novo logo após abrir um app legítimo
- **Defesas:**
  - manter o Android atualizado
  - desenvolvedores: taskAffinity vazio, intents explícitos, componentes não exportados
- **Referências:** OWASP M8

## ENG: Engenharia social e golpes

### ENG-01: Phishing por SMS (smishing) e mensageiros

- **Tática:** Acesso Inicial
- **Como acontece:** Mensagem urgente (entrega, banco, multa) com link para página falsa ou APK.
- **Sinais:** link encurtado ou domínio parecido com o oficial; pedido de instalar app por link
- **Defesas:**
  - nunca instalar app por link de mensagem
  - abrir o site digitando o endereço oficial
  - filtro de spam do app de mensagens
- **Referências:** MITRE: Acesso Inicial (phishing)

### ENG-02: Ligação falsa (vishing) e falsa central

- **Tática:** Acesso a Credenciais
- **Como acontece:** Golpista se passa pelo banco e pede código, senha ou para instalar app de 'proteção' ou acesso remoto.
- **Sinais:** pedido de código recebido por SMS; pedido de instalar app de acesso remoto
- **Defesas:**
  - banco não pede código nem senha por telefone: desligar e ligar para o número oficial
  - nunca instalar app de acesso remoto a pedido

### ENG-03: QR code malicioso (quishing)

- **Tática:** Acesso Inicial
- **Como acontece:** QR code colado sobre o legítimo leva a site falso ou a download de APK.
- **Sinais:** QR em adesivo sobreposto; endereço exibido diferente do esperado
- **Defesas:**
  - conferir o endereço antes de abrir
  - não instalar apps a partir de QR

### ENG-04: Falso suporte e apps de acesso remoto

- **Tática:** Comando e Controle
- **Como acontece:** Golpista convence a vítima a instalar um app legítimo de acesso remoto e opera o aparelho.
- **Sinais:** app de acesso remoto instalado recentemente sem uso seu
- **Defesas:**
  - desinstalar apps de acesso remoto que não usa
  - nunca dar código de sessão a quem ligou

### ENG-05: Golpe de engenharia social em redes e marketplaces

- **Tática:** Acesso Inicial
- **Como acontece:** Perfil falso, falsa venda ou falso emprego que leva a pagamento, código ou instalação.
- **Sinais:** pressa e pagamento fora da plataforma
- **Defesas:**
  - negociar só dentro da plataforma
  - desconfiar de urgência

## REDE: Rede e comunicação

### REDE-01: Homem no meio em Wi-Fi público ou falso (evil twin)

- **Tática:** Coleta
- **Como acontece:** Rede com o mesmo nome de uma conhecida intercepta ou altera o tráfego não cifrado.
- **Sinais:** aviso de certificado inválido; rede aberta com nome de estabelecimento
- **Defesas:**
  - preferir dados móveis ou VPN confiável em rede pública
  - esquecer redes abertas
  - nunca aceitar certificado inválido
- **Referências:** OWASP M5

### REDE-02: Certificado CA instalado pelo usuário (interceptação TLS)

- **Tática:** Coleta
- **Como acontece:** Um certificado raiz extra permite decifrar o tráfego de apps que confiam em certificados do usuário.
- **Sinais:** 'Credenciais do usuário' com certificado que você não instalou; aviso 'a rede pode estar sendo monitorada'
- **Defesas:**
  - Configurações > Segurança > Criptografia e credenciais > Credenciais do usuário: remover o desconhecido
- **Referências:** OWASP M5

### REDE-03: Proxy HTTP global configurado

- **Tática:** Coleta
- **Como acontece:** Proxy definido no sistema encaminha o tráfego por um servidor de terceiros.
- **Sinais:** proxy global definido nas configurações
- **Defesas:**
  - remover o proxy em Wi-Fi > rede > Proxy
  - via adb: settings put global http_proxy :0 (só se foi você que definiu)
- **Referências:** OWASP M5

### REDE-04: Sequestro de DNS

- **Tática:** Coleta
- **Como acontece:** Roteador ou rede comprometida responde endereços falsos para sites legítimos.
- **Sinais:** sites conhecidos pedindo login de novo ou com certificado estranho
- **Defesas:**
  - ativar DNS privado (DNS sobre TLS) em Configurações > Rede > DNS particular
- **Referências:** OWASP M5

### REDE-05: VPN maliciosa ou gratuita que vende dados

- **Tática:** Exfiltração
- **Como acontece:** O app de VPN vê todo o tráfego e pode registrar ou injetar conteúdo.
- **Sinais:** VPN desconhecida ativa; chave de VPN na barra de status sem você ter ligado
- **Defesas:**
  - usar só VPN de fornecedor confiável
  - remover VPNs que não usa

### REDE-06: Ataques por Bluetooth

- **Tática:** Movimento Lateral
- **Como acontece:** Falhas na pilha Bluetooth ou emparelhamentos indevidos permitem acesso ou rastreamento.
- **Sinais:** dispositivos emparelhados que você não reconhece
- **Defesas:**
  - desligar Bluetooth quando não usa
  - remover pareamentos desconhecidos
  - manter o patch em dia
- **Referências:** MITRE: Movimento Lateral

### REDE-07: NFC: retransmissão e leitura indevida

- **Tática:** Coleta
- **Como acontece:** Ataque de relay usa o NFC do aparelho ou do cartão para pagamento à distância curta.
- **Sinais:** NFC sempre ligado; app de pagamento desconhecido como padrão
- **Defesas:**
  - desligar NFC quando não usa
  - exigir desbloqueio para pagamento por aproximação

### REDE-08: Exploit sem clique (zero-click) por mensagem ou mídia

- **Tática:** Execução
- **Como acontece:** Arquivo de mídia ou mensagem malformada explora falha no processamento sem interação.
- **Sinais:** difícil de ver: o melhor sinal é patch atrasado
- **Defesas:**
  - patch de segurança em dia
  - atualizar apps de mensagem
  - Modo de Proteção Avançada (Android 16) para quem é alvo
- **Referências:** MITRE: Execução

## TEL: Telefonia e identidade

### TEL-01: Troca de chip (SIM swap)

- **Tática:** Acesso a Credenciais
- **Como acontece:** Golpista transfere o seu número para outro chip e recebe os códigos por SMS.
- **Sinais:** sinal de operadora some de repente; aviso de troca de chip
- **Defesas:**
  - PIN do chip
  - pedir à operadora bloqueio de portabilidade e troca
  - 2FA por app ou chave, não SMS

### TEL-02: Estação rádio-base falsa (IMSI catcher) e rebaixamento para 2G

- **Tática:** Coleta
- **Como acontece:** Antena falsa força o aparelho a 2G para interceptar chamadas e SMS.
- **Sinais:** aparelho caindo para 2G em área com 4G/5G
- **Defesas:**
  - desligar 2G em Rede móvel (Android 12+ em muitos aparelhos)

### TEL-03: Interceptação por SS7 e SMS como segundo fator

- **Tática:** Acesso a Credenciais
- **Como acontece:** Falhas da sinalização entre operadoras permitem desviar SMS.
- **Sinais:** códigos de verificação que você não pediu
- **Defesas:**
  - trocar SMS por app autenticador ou chave de acesso (passkey)

### TEL-04: Desvio de chamadas configurado sem você saber

- **Tática:** Coleta
- **Como acontece:** Códigos de operadora desviam chamadas (inclusive de verificação de banco) para outro número.
- **Sinais:** chamadas não chegam; ícone de desvio ativo
- **Defesas:**
  - conferir e cancelar desvios no discador (Configurações de chamada)

## SIS: Sistema, firmware e atualizações

### SIS-01: Patch de segurança desatualizado

- **Tática:** Escalada de Privilégio
- **Como acontece:** Falhas já públicas e corrigidas continuam exploráveis no aparelho sem atualização.
- **Sinais:** nível de patch com mais de 90 dias
- **Defesas:**
  - Configurações > Sistema > Atualização de software
  - atualizações do Google Play (sistema)
- **Referências:** Boletins de segurança do Android

### SIS-02: Aparelho sem suporte (fim de vida)

- **Tática:** Escalada de Privilégio
- **Como acontece:** O fabricante parou de publicar correções: toda falha nova fica aberta para sempre.
- **Sinais:** patch com mais de um ano; versão do Android antiga
- **Defesas:**
  - trocar o aparelho ou usar ROM mantida e auditada
  - reduzir apps e dados sensíveis nele

### SIS-03: Bootloader desbloqueado

- **Tática:** Persistência
- **Como acontece:** Permite gravar sistema modificado; quem pega o aparelho pode trocar o sistema.
- **Sinais:** verificação de boot laranja; ro.boot.flash.locked = 0
- **Defesas:**
  - rebloquear o bootloader com a imagem oficial (apaga os dados: fazer backup)

### SIS-04: Root (su, Magisk, KernelSU)

- **Tática:** Escalada de Privilégio
- **Como acontece:** Qualquer app com root lê tudo; malware explora root já existente.
- **Sinais:** binário su; app gerenciador de root instalado
- **Defesas:**
  - remover o root se não for indispensável
  - se mantiver, conceder root a pouquíssimos apps

### SIS-05: Firmware de origem duvidosa ou com chaves de teste

- **Tática:** Persistência
- **Como acontece:** Aparelhos baratos ou ROMs não oficiais vêm com malware de fábrica ou assinatura de teste.
- **Sinais:** ro.build.tags = test-keys; ro.debuggable = 1 num aparelho de usuário
- **Defesas:**
  - reinstalar firmware oficial
  - preferir aparelhos com Google Play Protect certificado
- **Referências:** OWASP M2

### SIS-06: Armazenamento sem criptografia

- **Tática:** Coleta
- **Como acontece:** Sem criptografia, quem tira o armazenamento lê os dados.
- **Sinais:** ro.crypto.state diferente de encrypted
- **Defesas:**
  - criptografia vem ligada no Android 10+; em aparelhos antigos, ativar em Segurança

### SIS-07: Play Protect desligado

- **Tática:** Evasão de Defesa
- **Como acontece:** Sem a verificação, apps maliciosos conhecidos não são bloqueados nem removidos.
- **Sinais:** verificação de apps desligada
- **Defesas:**
  - Play Store > Play Protect > Configurações: ligar 'Verificar apps'

## FIS: Acesso físico e periféricos

### FIS-01: Perda ou roubo do aparelho

- **Tática:** Acesso Inicial
- **Como acontece:** Quem tem o aparelho tenta desbloquear, trocar o chip e redefinir contas.
- **Sinais:** (físico)
- **Defesas:**
  - bloqueio de tela forte
  - Encontre Meu Dispositivo ligado
  - Proteção contra roubo do Google (bloqueio por detecção de roubo)
  - PIN do chip
  - anotar o IMEI

### FIS-02: Sem bloqueio de tela ou bloqueio fraco

- **Tática:** Acesso Inicial
- **Como acontece:** Qualquer pessoa com o aparelho na mão instala spyware em minutos.
- **Sinais:** bloqueio de tela desativado; padrão simples ou PIN curto
- **Defesas:**
  - PIN de 6+ dígitos ou senha
  - tempo de bloqueio curto
  - esconder notificações sensíveis na tela de bloqueio

### FIS-03: Depuração USB (ADB) e Opções do desenvolvedor ligadas

- **Tática:** Acesso Inicial
- **Como acontece:** Com ADB ligado, um computador autorizado instala e lê apps sem passar pela loja.
- **Sinais:** adb_enabled = 1 fora de uma sessão de uso seu
- **Defesas:**
  - desligar a depuração USB depois desta auditoria
  - revogar autorizações de depuração USB

### FIS-04: Carregador ou cabo malicioso (juice jacking)

- **Tática:** Acesso Inicial
- **Como acontece:** Porta de carregamento pública troca dados com o aparelho.
- **Sinais:** pedido de 'confiar neste computador' ao carregar
- **Defesas:**
  - usar carregador próprio
  - bloqueador de dados USB
  - manter 'só carregar' como padrão USB

### FIS-05: Acesso de pessoa próxima (parceiro, colega)

- **Tática:** Acesso Inicial
- **Como acontece:** Quem conhece o desbloqueio instala stalkerware ou lê conversas.
- **Sinais:** biometria de outra pessoa cadastrada; apps desconhecidos
- **Defesas:**
  - trocar o PIN
  - conferir digitais e rostos cadastrados
  - Verificação de segurança do Google

## PRIV: Privacidade e rastreamento

### PRIV-01: Rastreamento de localização

- **Tática:** Coleta
- **Como acontece:** Apps com localização em segundo plano reconstroem a sua rotina.
- **Sinais:** localização 'Permitir o tempo todo' em vários apps
- **Defesas:**
  - localização 'Só durante o uso' ou 'Perguntar'
  - localização aproximada quando bastar
- **Referências:** OWASP M6

### PRIV-02: Rastreador físico escondido (tag Bluetooth)

- **Tática:** Coleta
- **Como acontece:** Tag de rastreamento colocada na bolsa ou no carro.
- **Sinais:** alerta de rastreador desconhecido
- **Defesas:**
  - manter os alertas de rastreadores desconhecidos ligados
  - fazer a varredura manual de rastreadores

### PRIV-03: SDKs de publicidade e corretores de dados

- **Tática:** Exfiltração
- **Como acontece:** Bibliotecas dentro de apps legítimos coletam identificadores e localização.
- **Sinais:** apps gratuitos com muitas permissões
- **Defesas:**
  - apagar o ID de publicidade
  - revisar a seção de Segurança dos dados na loja
- **Referências:** OWASP M2; OWASP M6

### PRIV-04: Área de transferência lida por outros apps

- **Tática:** Coleta
- **Como acontece:** Apps leem o que você copiou (senhas, chaves de carteira).
- **Sinais:** aviso 'app colou da área de transferência' (Android 12+)
- **Defesas:**
  - não copiar senhas; usar gerenciador com preenchimento automático

### PRIV-05: Câmera e microfone acessados às escondidas

- **Tática:** Coleta
- **Como acontece:** App em segundo plano liga sensores.
- **Sinais:** ponto verde de câmera/microfone sem uso seu
- **Defesas:**
  - bloqueio rápido de câmera e microfone (Android 12+)
  - revogar a permissão

## CONTA: Contas e nuvem

### CONTA-01: Tomada da conta Google

- **Tática:** Acesso a Credenciais
- **Como acontece:** Com a conta, o atacante localiza, apaga e lê backups do aparelho.
- **Sinais:** alertas de login novo; aparelhos desconhecidos na conta
- **Defesas:**
  - chave de acesso (passkey) ou 2FA forte
  - Verificação de segurança do Google
  - remover aparelhos desconhecidos

### CONTA-02: Sequestro de WhatsApp e mensageiros

- **Tática:** Acesso a Credenciais
- **Como acontece:** Golpista pede o código de verificação e registra a sua conta em outro aparelho.
- **Sinais:** pedido de código de 6 dígitos por terceiros
- **Defesas:**
  - confirmação em duas etapas (PIN) no mensageiro
  - nunca repassar código

### CONTA-03: Reutilização de senha e vazamentos

- **Tática:** Acesso a Credenciais
- **Como acontece:** Senha vazada em um site é testada em todos os outros.
- **Sinais:** alerta de senha comprometida do gerenciador
- **Defesas:**
  - gerenciador de senhas
  - uma senha por site
  - Verificação de senhas do Google

### CONTA-04: Backup na nuvem acessado por terceiros

- **Tática:** Exfiltração
- **Como acontece:** Com a conta, o backup de mensagens e fotos é baixado.
- **Sinais:** (conta)
- **Defesas:**
  - backup cifrado de ponta a ponta quando o app oferece
  - proteger a conta (CONTA-01)

## APP: Falhas de apps (OWASP Mobile Top 10 2024)

### APP-M1: M1 Uso impróprio de credenciais

- **Tática:** Acesso a Credenciais
- **Como acontece:** Chaves de API e senhas embutidas no app ou guardadas sem proteção.
- **Sinais:** (desenvolvimento)
- **Defesas:**
  - sem segredos no APK
  - Android Keystore
  - tokens de curta duração
- **Referências:** OWASP M1 (2024)

### APP-M2: M2 Cadeia de suprimentos inadequada

- **Tática:** Acesso Inicial
- **Como acontece:** Bibliotecas e SDKs de terceiros comprometidos ou vulneráveis.
- **Sinais:** (desenvolvimento)
- **Defesas:**
  - inventário de dependências (SBOM)
  - fixar versões e conferir assinaturas
- **Referências:** OWASP M2 (2024)

### APP-M3: M3 Autenticação e autorização inseguras

- **Tática:** Acesso a Credenciais
- **Como acontece:** Decisões de acesso feitas só no cliente.
- **Sinais:** (desenvolvimento)
- **Defesas:**
  - autorizar no servidor
  - biometria ligada a chave criptográfica
- **Referências:** OWASP M3 (2024)

### APP-M4: M4 Validação insuficiente de entrada e saída

- **Tática:** Execução
- **Como acontece:** Injeção por intents, deep links, WebView e dados do servidor.
- **Sinais:** (desenvolvimento)
- **Defesas:**
  - validar todo dado externo
  - WebView sem JavaScript bridge exposto
- **Referências:** OWASP M4 (2024)

### APP-M5: M5 Comunicação insegura

- **Tática:** Coleta
- **Como acontece:** HTTP sem TLS, validação de certificado desligada.
- **Sinais:** (desenvolvimento)
- **Defesas:**
  - TLS sempre
  - Network Security Config sem cleartext
  - pinning onde fizer sentido
- **Referências:** OWASP M5 (2024)

### APP-M6: M6 Controles de privacidade inadequados

- **Tática:** Coleta
- **Como acontece:** Coleta além do necessário, logs com dados pessoais.
- **Sinais:** (desenvolvimento)
- **Defesas:**
  - minimização de dados
  - nada pessoal em logs
- **Referências:** OWASP M6 (2024)

### APP-M7: M7 Proteção binária insuficiente

- **Tática:** Evasão de Defesa
- **Como acontece:** App fácil de reempacotar e adulterar.
- **Sinais:** (desenvolvimento)
- **Defesas:**
  - Play Integrity API
  - ofuscação (R8)
  - verificação de assinatura no servidor
- **Referências:** OWASP M7 (2024)

### APP-M8: M8 Configuração de segurança incorreta

- **Tática:** Evasão de Defesa
- **Como acontece:** Componentes exportados, allowBackup, debuggable em produção.
- **Sinais:** (desenvolvimento)
- **Defesas:**
  - exported=false por padrão
  - debuggable=false
  - permissões de assinatura em componentes
- **Referências:** OWASP M8 (2024)

### APP-M9: M9 Armazenamento de dados inseguro

- **Tática:** Coleta
- **Como acontece:** Dados sensíveis em armazenamento externo ou sem cifra.
- **Sinais:** (desenvolvimento)
- **Defesas:**
  - armazenamento interno
  - EncryptedFile / Keystore
- **Referências:** OWASP M9 (2024)

### APP-M10: M10 Criptografia insuficiente

- **Tática:** Acesso a Credenciais
- **Como acontece:** Algoritmos fracos, chaves fixas, modos inseguros.
- **Sinais:** (desenvolvimento)
- **Defesas:**
  - AES-GCM com chaves do Keystore
  - nunca criptografia caseira
- **Referências:** OWASP M10 (2024)

## SUP: Cadeia de suprimentos

### SUP-01: Malware pré-instalado de fábrica

- **Tática:** Persistência
- **Como acontece:** Firmware de aparelhos e TV boxes baratos já vem com backdoor.
- **Sinais:** apps de sistema desconhecidos que não podem ser removidos
- **Defesas:**
  - comprar aparelhos certificados pelo Play Protect
  - desativar apps de sistema suspeitos
- **Referências:** OWASP M2

### SUP-02: Atualização maliciosa de app legítimo

- **Tática:** Execução
- **Como acontece:** App confiável é vendido ou comprometido e recebe uma atualização maliciosa.
- **Sinais:** app antigo passa a pedir permissões novas
- **Defesas:**
  - desconfiar de pedidos novos de permissão depois de uma atualização
  - remover apps abandonados
- **Referências:** OWASP M2

## DADO: Dados no aparelho

### DADO-01: Arquivos sensíveis no armazenamento compartilhado

- **Tática:** Coleta
- **Como acontece:** Documentos e fotos em pastas que qualquer app com acesso a arquivos lê.
- **Sinais:** apps com 'Acesso a todos os arquivos'
- **Defesas:**
  - revogar 'Gerenciar todos os arquivos'
  - usar a pasta segura (Espaço privado no Android 15+)

### DADO-02: Dados restantes em aparelho vendido ou descartado

- **Tática:** Exfiltração
- **Como acontece:** Contas e arquivos ficam no aparelho que muda de dono.
- **Sinais:** (descarte)
- **Defesas:**
  - remover a conta Google antes
  - restauração de fábrica com criptografia ligada

## Defesas gerais

1. Manter o Android e as atualizações do Google Play sempre em dia (o maior redutor de risco isolado).
2. Instalar apps só da Play Store ou da loja oficial do fabricante; nunca por link de mensagem.
3. Play Protect ligado, inclusive a verificação de apps instalados por USB.
4. Bloqueio de tela com PIN de 6+ dígitos ou senha; biometria como conveniência, não como única barreira.
5. Revisar mensalmente: Acessibilidade, Administradores do dispositivo, Acesso a notificações, Sobreposição, Instalar apps desconhecidos.
6. Permissões no mínimo: 'só durante o uso' para localização, câmera e microfone; revogar SMS e registro de chamadas de quem não precisa.
7. Chaves de acesso (passkeys) ou app autenticador no lugar de SMS; PIN no chip; confirmação em duas etapas nos mensageiros.
8. Encontre Meu Dispositivo e proteções contra roubo ligados.
9. DNS particular (DNS sobre TLS) e cuidado com Wi-Fi público; nenhum certificado de usuário desconhecido.
10. Depuração USB e Opções do desenvolvedor desligadas quando não estão em uso.
11. Bootloader bloqueado e sem root, salvo necessidade real.
12. Backups regulares e cifrados, fora do aparelho.
13. Para pessoas em risco elevado: Modo de Proteção Avançada (Android 16+) e chave de segurança física na conta.
14. Em caso de comprometimento grave: trocar senhas de OUTRO aparelho, depois restauração de fábrica, depois reinstalar só o necessário.

## Fontes

- MITRE ATT&CK Mobile: https://attack.mitre.org/matrices/mobile/
- OWASP Mobile Top 10 (2024): https://owasp.org/www-project-mobile-top-10/
- Indicadores de stalkerware (Echap): https://github.com/AssoEchap/stalkerware-indicators
