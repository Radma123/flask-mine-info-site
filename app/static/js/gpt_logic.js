document.getElementById('new-chat-button').addEventListener('click', async function(){
    document.getElementById("chat-place").replaceChildren();
    if (isAuthenticated) {
        console.log('Authenticated')
    }
});


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

        const ulElement = document.querySelector('.conversations-to-choice');
        if (isAuthenticated){
            const user_id = document.querySelector(".user_nickname").getAttribute("value");
            const model = document.getElementById('gpt_value').value;
            const user_message = text
            const bot_message = botMessage.textContent

            if (ulElement.childElementCount == 0) {
                let response = await fetch("/create_chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ "user_id": user_id, "model": model, "user_message": user_message, "bot_message": bot_message })
                });
            
                let result = await response.json();

                // // Создаем новый элемент li
                // const liElement = document.createElement('li');
                // liElement.classList.add('choice-element');
    
                // // Добавляем кнопки в новый li
                // const button1 = document.createElement('a');
                // button1.classList.add('btn', 'btn-light', 'conversations-to-choice-button', 'text-truncate');
                // button1.textContent = document.getElementById('chat-place').getElementsByClassName('user-message')[0].textContent
                
                // const button2 = document.createElement('button');
                // button2.type = 'button';
                // button2.classList.add('btn', 'btn-light', 'delete-button');
                
                // const icon = document.createElement('i');
                // icon.classList.add('bi', 'bi-trash3');
                // button2.appendChild(icon);
                
                // // Добавляем кнопки в li
                // liElement.appendChild(button1);
                // liElement.appendChild(button2);
                
                // // Добавляем новый li в ul
                // ulElement.appendChild(liElement);
            }else{
                console.log(ulElement.childElementCount);
            }

            
    
        }
    } else {
        alert("Ошибка при отправке (попробуйте выбрать другую модель): " + result.message);
    }
    
});

