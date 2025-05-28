function Component()
{
    // Constructeur par défaut
}

Component.prototype.createOperations = function()
{
    try {
        // Appel à la méthode parente
        component.createOperations();

        if (systemInfo.productType === "windows") {
            // Création d'un raccourci dans le menu démarrer
            component.addOperation("CreateShortcut", 
                "@TargetDir@/chocolat.bat", 
                "@StartMenuDir@/Chocolat Panel.lnk",
                "workingDirectory=@TargetDir@",
                "iconPath=%SystemRoot%/system32/SHELL32.dll",
                "iconId=2"
            );
            
            // Création d'un raccourci sur le bureau
            component.addOperation("CreateShortcut", 
                "@TargetDir@/chocolat.bat", 
                "@DesktopDir@/Chocolat Panel.lnk",
                "workingDirectory=@TargetDir@",
                "iconPath=%SystemRoot%/system32/SHELL32.dll",
                "iconId=2"
            );
            
            // Créer les répertoires nécessaires pour les fichiers de configuration
            component.addOperation("Mkdir", "@HomeDir@/Ona");
            component.addOperation("Mkdir", "@HomeDir@/Ona/var");
            component.addOperation("Mkdir", "@HomeDir@/Ona/var/persistent");
            
            // Installer Python si nécessaire (commenté car généralement mieux fait avec un prérequis)
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
            // Proposer de lancer l'application après l'installation
            if (systemInfo.productType === "windows") {
                installer.executeDetached("@TargetDir@/chocolat.bat");
            }
        }
    } catch (e) {
        console.log(e);
    }
}