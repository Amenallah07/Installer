function Component() {}

Component.prototype.createOperations = function()
{
    try {
        
	component.createOperations();

        if (systemInfo.productType === "windows") {
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

            // (optionnel) Installation of Python
            // component.addOperation("Execute", "@TargetDir@/prerequisites/python-3.9.10-amd64.exe", "/quiet", "InstallAllUsers=1", "PrependPath=1");
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
