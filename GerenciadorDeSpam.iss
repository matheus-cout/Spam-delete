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
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Guia de Configuração"; Filename: "{app}\configuracao_exclusao_automatica_spam.md"
Name: "{group}\README"; Filename: "{app}\README_SPAM_DELETION.md"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
// Função para verificar se o Gmail está configurado no sistema
function IsGmailConfigured(): Boolean;
begin
  // Esta é uma função simplificada. Em um cenário real, você poderia
  // verificar se o Outlook ou outro cliente de email está configurado com Gmail
  Result := True;
end;

// Função para exibir informações adicionais durante a instalação
procedure InitializeWizard;
var
  InfoPage: TNewNotebookPage;
  InfoLabel: TLabel;
begin
  // Criar uma página de informações
  InfoPage := WizardForm.PagesNotebook.Add;

  // Adicionar um rótulo com informações
  InfoLabel := TLabel.Create(WizardForm);
  InfoLabel.Parent := InfoPage;
  InfoLabel.Left := WizardForm.ClientWidth div 10;
  InfoLabel.Top := WizardForm.ClientHeight div 4;
  InfoLabel.Width := WizardForm.ClientWidth * 8 div 10;
  InfoLabel.Height := WizardForm.ClientHeight div 2;
  InfoLabel.Caption := 'O Gerenciador de Spam do Gmail é uma ferramenta que permite verificar e excluir emails de spam automaticamente.' + #13#10#13#10 +
                       'Para usar esta ferramenta, você precisa ter uma conta do Gmail e ter configurado uma senha de aplicativo.' + #13#10#13#10 +
                       'Após a instalação, você pode configurar o programa para ser executado automaticamente em intervalos regulares usando o Agendador de Tarefas do Windows.';

  // Adicionar a página ao assistente
  WizardForm.PagesNotebook.SelectPage(InfoPage.Index);
end;
