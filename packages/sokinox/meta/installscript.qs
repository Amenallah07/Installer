function Component() {}

Component.prototype.createOperations = function()
{
    try {
        
	component.createOperations();

        if (systemInfo.productType === "windows") {
            // Check if Python is installed, if not install it
            var pythonInstaller = "@TargetDir@/bin/python-3.13.3-amd64.exe";
            component.addOperation("Execute", "python", "--version", "UNDOEXECUTE", "echo", "Python check");
            component.addOperation("Execute", "{0,1}", "cmd", "/c", "python --version || \"" + pythonInstaller + "\" /quiet InstallAllUsers=1 PrependPath=1");

            // Start menu shortcut
            component.addOperation("CreateShortcut", 
                "@TargetDir@/chocolat.bat", 
                "@StartMenuDir@/Sokinox Simulator.lnk",
                "workingDirectory=@TargetDir@",
                "iconPath=@TargetDir@/icons/icon.ico",
                "iconId=0"
            );

            // Desktop shortcut
            component.addOperation("CreateShortcut", 
                "@TargetDir@/chocolat.bat", 
                "@DesktopDir@/Sokinox Simulator.lnk",
                "workingDirectory=@TargetDir@",
                "iconPath=@TargetDir@/icons/icon.ico",
                "iconId=0"
            );

            // Customized directories
            component.addOperation("Mkdir", "C:/Ona");
            component.addOperation("Mkdir", "C:/Ona/var");
            component.addOperation("Mkdir", "C:/Ona/var/persistent");
        }
    } catch (e) {
        console.log(e);
    }
}

Component.prototype.installationFinished = function()
{
    try {
        if (installer.isInstaller() && installer.status == QInstaller.Success) {
            if (systemInfo.productType === "windows") {
                installer.executeDetached("@TargetDir@/chocolat.bat");
            }
        }
    } catch (e) {
        console.log(e);
    }
}
