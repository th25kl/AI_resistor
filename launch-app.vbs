Option Explicit

Dim shell, projectPath, electronPath, command
Set shell = CreateObject("WScript.Shell")
projectPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
electronPath = projectPath & "\node_modules\electron\dist\electron.exe"
command = """" & electronPath & """ """ & projectPath & """"
shell.Run command, 0, False
