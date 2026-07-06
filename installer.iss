#define MyAppName "CodeMaster AI"
#define MyAppVersion "1.0"
#define MyAppPublisher "Valentine Achieng"
#define MyAppExeName "CodeMasterAI.exe"

[Setup]
AppId={{A8F22C8B-5C81-4A5E-BF8F-3E84C6E4B101}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=Installer
OutputBaseFilename=CodeMasterAI_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist\CodeMasterAI.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CodeMaster AI"; Filename: "{app}\CodeMasterAI.exe"
Name: "{autodesktop}\CodeMaster AI"; Filename: "{app}\CodeMasterAI.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\CodeMasterAI.exe"; Description: "Launch CodeMaster AI"; Flags: nowait postinstall skipifsilent
