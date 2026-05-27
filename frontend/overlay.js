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

    document.body.innerHTML = `

    <div class="overlay">

        <div class="portrait-container">

            <img
                class="portrait"
                src="/frontend/assets/portraits/${playerName}.png"
                onerror="this.onerror=null; this.src='https://placehold.co/200x200';"
            >

            <div class="energy-circle">

                ${player.energy}

            </div>

        </div>

        <div class="info">

            <div class="name">
                ${player.displayName}
            </div>

            <div class="bar">

                <div
                    class="fill hp-fill"
                    style="
                        width:
                        ${(player.hp / player.maxHp) * 100}%
                    "
                ></div>

                <div class="bar-text">
                    HP:
                    ${player.hp}
                    /
                    ${player.maxHp}
                </div>

            </div>

            <div class="bar">

                <div
                    class="fill mental-fill"
                    style="
                        width:
                        ${(player.mental / player.maxMental) * 100}%
                    "
                ></div>

                <div class="bar-text">
                    Mental:
                    ${player.mental}
                    /
                    ${player.maxMental}
                </div>

            </div>

        </div>

    </div>

    `
}