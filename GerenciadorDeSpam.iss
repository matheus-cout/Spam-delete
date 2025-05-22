#define MyAppName "Gerenciador de Spam do Gmail"
#define MyAppVersion "1.0"
#define MyAppPublisher "Seu Nome ou Empresa"
#define MyAppURL "https://seusite.com.br"
#define MyAppExeName "GerenciadorDeSpam.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{A1B2C3D4-E5F6-4A5B-9C8D-7E6F5A4B3C2D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=instalador
OutputBaseFilename=GerenciadorDeSpam_Setup
Compression=lzma
SolidCompression=yes
; Configurações de interface
WizardStyle=modern
; Configurações de privilégios
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
; Arquivo de licença
LicenseFile=licenca.txt
; Ícones
SetupIconFile=icones\gerenciador_spam.ico

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "build\exe.win-amd64-3.13\GerenciadorDeSpam.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "build\exe.win-amd64-3.13\python313.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "build\exe.win-amd64-3.13\README_SPAM_DELETION.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "build\exe.win-amd64-3.13\configuracao_exclusao_automatica_spam.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "build\exe.win-amd64-3.13\lib\*"; DestDir: "{app}\lib"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "icones\gerenciador_spam.ico"; DestDir: "{app}\icones"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icones\gerenciador_spam.ico"
Name: "{group}\Guia de Configuração"; Filename: "{app}\configuracao_exclusao_automatica_spam.md"
Name: "{group}\README"; Filename: "{app}\README_SPAM_DELETION.md"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icones\gerenciador_spam.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icones\gerenciador_spam.ico"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Messages]
WelcomeLabel2=Este assistente irá guiá-lo através da instalação do [name].%n%nO Gerenciador de Spam do Gmail é uma ferramenta que permite verificar e excluir emails de spam automaticamente.%n%nPara usar esta ferramenta, você precisa ter uma conta do Gmail e ter configurado uma senha de aplicativo.%n%nApós a instalação, você pode configurar o programa para ser executado automaticamente em intervalos regulares usando o Agendador de Tarefas do Windows.
FinishedLabel=A instalação do [name] foi concluída com sucesso.%n%nClique em Concluir para sair do assistente de instalação.
