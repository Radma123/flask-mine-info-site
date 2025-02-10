document.addEventListener("DOMContentLoaded", function() {
    if (!isAuthenticated) {
        let select = document.getElementById("gpt_value");

        // Загружаем последний выбор из localStorage
        let savedModel = localStorage.getItem("selectedModel");
        if (savedModel && select.querySelector(`option[value="${savedModel}"]`)) {
            select.value = savedModel;
        }

        // Обработчик изменений
        select.addEventListener("change", function() {
            localStorage.setItem("selectedModel", select.value);
        });
    }
});


document.getElementById("floatingTextarea").addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) { // Enter без Shift
        event.preventDefault(); // Отмена стандартного переноса строки
        document.getElementById("sendButton").click(); // Кликаем кнопку отправки
    }
});


document.getElementById("sendButton").addEventListener("click", async function() {
    let text = document.getElementById("floatingTextarea").value;
    let sendButton = document.getElementById("sendButton");
    let selectedGPT = document.getElementById("gpt_value").value;
    let chatPlace = document.querySelector(".chat-place");

    if (!text.trim()) return; // Игнорируем пустой ввод

    // Заменяем иконку отправки на спиннер
    sendButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    sendButton.disabled = true;

    let userMessage = document.createElement("div");
    userMessage.classList.add("message", "user-message"); // Можно стилизовать
    userMessage.textContent = text;
    chatPlace.appendChild(userMessage);
    
    chatPlace.scrollTop = chatPlace.scrollHeight;

    try {
        // Отправка данных на сервер
        let response = await fetch("/send", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text, gpt: selectedGPT })
        });

        let result = await response.json();
        
        // Вернуть кнопку в исходное состояние
        sendButton.innerHTML = '<i class="h1 bi bi-send"></i>';
        sendButton.disabled = false;
        
        if (result.status === 'success') {
            document.getElementById("floatingTextarea").value = ""; // Очистка поля
            let botMessage = document.createElement("div");
            botMessage.classList.add("message", "bot-message");
            botMessage.textContent = result.message;
            chatPlace.appendChild(botMessage);
            chatPlace.scrollTop = chatPlace.scrollHeight;
            console.log(11)

            if (isAuthenticated){
                const chatElement = document.getElementById('chat-place');
                console.log(22);
                const model = document.getElementById('gpt_value').value;
                const user_message = text;
                const bot_message = botMessage.textContent;

                if (chatElement.childElementCount == 2) {
                    console.log(33);
                    let response = await fetch("/gpt/create_chat", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({"model": model, "user_message": user_message, "bot_message": bot_message })
                    });
                
                    let result = await response.json();
                    console.log(44);
                    console.log('/'+result.chat_id);
                    window.location.href = '/gpt/'+result.chat_id;

                }else{
                    console.log(chatElement.childElementCount);
                    const lastSegment = window.location.pathname.split('/').filter(Boolean).pop();
                    let response = await fetch("/gpt/"+lastSegment+"/add", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({"model": model, "user_message": user_message, "bot_message": bot_message })
                    });
                }

                
        
            }else{
                console.log('User is not authentificated, history will not be saved');
            }

        } else {
            alert("Ошибка при отправке (попробуйте выбрать другую модель): " + result.message);
        }
    }catch(err) {
        console.error("Ошибка при отправке запроса:", err);
        alert("Ошибка сети. Проверьте соединение и попробуйте снова.");
        sendButton.innerHTML = '<i class="h1 bi bi-send"></i>';
        sendButton.disabled = false;
    }
});

