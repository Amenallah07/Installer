function Component() {}

Component.prototype.createOperations = function()
{
    try {
        component.createOperations();

        if (systemInfo.productType === "windows") {
            // Installer Python de manière silencieuse (même s'il existe déjà)
            // L'installateur Python détecte automatiquement s'il est déjà installé
            component.addOperation("Execute", "{0,1}",
                "@TargetDir@/python-3.13.3-amd64.exe",
                "/quiet", "InstallAllUsers=1", "PrependPath=1");

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

            // Améliorer l'enregistrement dans le registre Windows
            var registryKey = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{" + installer.value("ProductUUID") + "}";

            component.addOperation("GlobalConfig",
                registryKey,
                "DisplayName", "Sokinox Simulator");

            component.addOperation("GlobalConfig",
                registryKey,
                "DisplayVersion", "@Version@");

            component.addOperation("GlobalConfig",
                registryKey,
                "Publisher", "InoSystemes");

            component.addOperation("GlobalConfig",
                registryKey,
                "InstallLocation", "@TargetDir@");

            component.addOperation("GlobalConfig",
                registryKey,
                "UninstallString", "\"@TargetDir@/@MaintenanceToolName@.exe\"");

            component.addOperation("GlobalConfig",
                registryKey,
                "QuietUninstallString", "\"@TargetDir@/@MaintenanceToolName@.exe\" --script uninstall.qs");

            component.addOperation("GlobalConfig",
                registryKey,
                "DisplayIcon", "@TargetDir@/icons/icon.ico");

            component.addOperation("GlobalConfig",
                registryKey,
                "NoModify", "1");

            component.addOperation("GlobalConfig",
                registryKey,
                "NoRepair", "1");
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
