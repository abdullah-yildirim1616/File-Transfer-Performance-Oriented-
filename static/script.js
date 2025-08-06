document.addEventListener("DOMContentLoaded", function() {
    loadDirectory("");

    function loadDirectory(path) {
        fetch("/list-dir/" + path)
            .then(response => response.json())
            .then(data => {
                document.getElementById("folder-view").innerHTML = "<h3>📂 Folders</h3>";
                document.getElementById("file-view").innerHTML = "<h3>📄 Files</h3>";

                data.folders.forEach(folder => {
                    const folderItem = document.createElement("div");
                    folderItem.innerHTML = `<a href="#" onclick="loadDirectory('${folder.path}')">${folder.name}</a>`;
                    document.getElementById("folder-view").appendChild(folderItem);
                });

                data.files.forEach(file => {
                    const fileItem = document.createElement("div");
                    fileItem.innerHTML = `${file.name} (${(file.size / 1024).toFixed(1)} KB) - <a href="/download/${file.path}">Download</a>`;
                    document.getElementById("file-view").appendChild(fileItem);
                });
            });
    }

    window.loadDirectory = loadDirectory;
});
