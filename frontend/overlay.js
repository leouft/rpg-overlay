const ws =
    new WebSocket("ws://localhost:8000/ws")

const path =
    window.location.pathname

const playerName =
    path.split("/")[2]

ws.onmessage = (event) => {

    const players =
        JSON.parse(event.data)

    const player =
        players[playerName]

    if (!player) return

    console.log(player)

    document.body.innerHTML = `

    <div class="overlay">

        <div class="portrait-container">

            <img
                class="portrait"
                src="/frontend/assets/portraits/${playerName}.png"
                onerror="this.onerror=null; this.src='https://placehold.co/200x200';"
            >

            <div class="courage-circle">

                ${player.courage}

            </div>

        </div>

        <div class="info">

            <div class="name">
                ${player.displayName}
            </div>

            <div class="bar">

                <div
                    class="fill pe-fill"
                    style="
                        width:
                        ${(player.peCurrent / player.peMax) * 100}%
                    "
                ></div>

                <div class="bar-text">
                    PE:
                    ${player.peCurrent}
                    /
                    ${player.peMax}
                </div>

            </div>

            <div class="bar">

                <div
                    class="fill knockout-fill"
                    style="
                        width:
                        ${(player.knockout / 3) * 100}%
                    "
                ></div>

                <div class="bar-text">
                    Fora de ação:
                    ${player.knockout}
                    /
                    ${3}
                </div>

            </div>

        </div>

    </div>

    `
}