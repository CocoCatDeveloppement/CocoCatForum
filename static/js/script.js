document.addEventListener("DOMContentLoaded", function(){
    const container = document.getElementById("conteneur-message");
    const messages = Array.from(container.getElementsByClassName('message'));
    messages.sort((a,b) => {
        const likeA = parseInt(a.querySelector('.likeButton').innerText);
        const likeB = parseInt(b.querySelector('.likeButton').innerText);

        return likeB - likeA;
    });

    container.innerHTML = "";
    messages.forEach(msg => 
        container.appendChild(msg));
});