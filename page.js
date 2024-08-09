const urlParams = new URLSearchParams(window.location.search);
const manga = urlParams.get('manga');
const chapter = urlParams.get('chapter');
const mangaName = document.getElementById("mangaName");
const scrollButton = document.getElementById("controls").children[0];
const nextButton = document.getElementById("controls").children[1];

if (manga == null) {
    nextButton.remove();
    fetch("/get_mangas",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                url: window.location.href
            })
        }
    ).then(
        function (response) {
            return response.json();
        }
    ).then(
        function (data) {
            console.log(data);
            for (let i = 0; i < data.length; i++) {
                let mangaLink = document.createElement("a");
                mangaLink.href = "/page.html?manga=" + data[i];
                mangaLink.innerText = data[i];
                document.getElementById("panels").appendChild(mangaLink);
            }
        }
    )
} else if (chapter == null) {
    nextButton.remove();
    mangaName.innerText = manga;
    fetch("/get_pages",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                manga: manga
            },
            body: JSON.stringify({
                url: window.location.href
            })
        }
    ).then(
        function (response) {
            return response.json();
        }
    ).then(
        function (data) {
            for (let i = 0; i < data; i++) {
                let chapterLink = document.createElement("a");
                chapterLink.href = "/page.html?manga=" + manga + "&chapter=" + (i + 1);
                chapterLink.innerText = "Chapter " + (i + 1);
                document.getElementById("panels").appendChild(chapterLink);
            }
        }
    )
} else {
    let scrollInterval;
    nextButton.onclick = function () {
        window.location.href = "/page.html?manga=" + manga + "&chapter=" + (parseInt(chapter) + 1);
    }
    scrollButton.addEventListener("mousedown", function (e) {scrollInterval = setInterval(function () {window.scrollBy(0, 10);}, 10); e.preventDefault();})
    scrollButton.addEventListener("contextmenu", function(event) {event.preventDefault();});
    scrollButton.addEventListener("touchstart", function (e) {scrollInterval = setInterval(function () {window.scrollBy(0, 10);}, 10);e.preventDefault();})
    scrollButton.addEventListener("mouseup", function (e) {clearInterval(scrollInterval);e.preventDefault();})
    scrollButton.addEventListener("mouseleave", function (e) {clearInterval(scrollInterval);e.preventDefault();})
    scrollButton.addEventListener("touchend", function (e) {clearInterval(scrollInterval);e.preventDefault();})

    mangaName.innerText = manga + " - Chapter " + chapter;
    fetch("/get_panels",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                manga: manga,
                chapter: chapter
            },
            body: JSON.stringify({
                url: window.location.href
            })
        }
    ).then(
        function (response) {
            return response.json();
        }
    ).then(
        function (data) {
            console.log(data);
            for (let i = 0; i < data.length; i++) {
                let img = document.createElement("img");
                img.src = data[i];
                document.getElementById("panels").appendChild(img);
            }
        }
    )
}
