async function chargerMessages() {
    const res = await fetch("/messages_json");
    const messages = await res.json();

    const groupes = {};

    messages.forEach(msg => {
        if (!groupes[msg.sujet]) groupes[msg.sujet] = [];
        groupes[msg.sujet].push(msg);
    });

    afficherGroupes(groupes);
}

function afficherGroupes(groupes) {
    const conteneur = document.getElementById("conteneur-message");
    conteneur.innerHTML = "";

    for (const sujet in groupes) {
        const bloc = document.createElement("div");
        bloc.className = "sujet-bloc";

        bloc.innerHTML = `<h2>${sujet}</h2>`;

        groupes[sujet].forEach(msg => {
            bloc.innerHTML += `
                <div class="message">
                    <p><strong>${msg.pseudo}</strong></p>
                    <p>${msg.message}</p>
                    <p>${msg.date}</p>

                    <button class="like-btn" data-id="${msg.id}">
                        ${msg.likes} ❤️
                    </button>
                </div>
            `;
        });

        conteneur.appendChild(bloc);
    }

    activerLikes();
}

function activerLikes() {
    document.querySelectorAll(".like-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;

            const res = await fetch("/like", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id })
            });

            const data = await res.json();
            btn.innerHTML = `${data.likes} ❤️`;

            chargerMessages();
        });
    });
}

document.addEventListener("DOMContentLoaded", chargerMessages);

