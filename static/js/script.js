function trierMessages() {
    const container = document.getElementById("conteneur-message");
    const messages = Array.from(container.getElementsByClassName('message'));

    messages.sort((a, b) => {
        const likeA = parseInt(a.querySelector('.likeButton').innerText);
        const likeB = parseInt(b.querySelector('.likeButton').innerText);
        return likeB - likeA;
    });

    container.innerHTML = "";
    messages.forEach(msg => container.appendChild(msg));
}

document.addEventListener("DOMContentLoaded", function() {
    trierMessages();
});

document.querySelectorAll(".like-form").forEach(form => {
    form.querySelector(".like-btn").addEventListener("click", async () => {

        const id = form.dataset.id;

        const response = await fetch("/like", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: id })
        });

        const data = await response.json();

        // Mise à jour instantanée du compteur
        form.querySelector(".likeButton").innerText = data.likes;

        // 🔥 Animation POP
        const btn = form.querySelector(".like-btn");
        btn.classList.add("pop");
        setTimeout(() => btn.classList.remove("pop"), 150);

        // Relancer le tri
        trierMessages();
    });
});


