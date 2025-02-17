//загрузка последней модели из localStorage
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

//реакция на Enter
document.getElementById("floatingTextarea").addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) { // Enter без Shift
        event.preventDefault(); // Отмена стандартного переноса строки
        document.getElementById("sendButton").click(); // Кликаем кнопку отправки
    }
});

//запуск скрипта обработки нажатия
document.getElementById("sendButton").addEventListener("click", async function() {
    let text = document.getElementById("floatingTextarea").value;
    let sendButton = document.getElementById("sendButton");
    let selectedGPT = document.getElementById("gpt_value").value;
    let chatPlace = document.querySelector(".chat-place");

    let dataUploaded = document.getElementById('custom-file-label').getAttribute('data-uploaded');
    let photo = null;
    let generate_img_mode = document.getElementById('custom-file-label').hidden

    if (!text.trim()) return; // Игнорируем пустой ввод

    // Заменяем иконку отправки на спиннер
    sendButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    sendButton.disabled = true;

    let userMessage = document.createElement("div");
    userMessage.classList.add("message", "user-message"); // Можно стилизовать
    userMessage.textContent = text;
    chatPlace.appendChild(userMessage);

    if (!generate_img_mode) {
        if (dataUploaded == "true") {
            photo = document.getElementById('fileInput').files[0];
            let reader = new FileReader();
    
            let photo_base64 = await new Promise((resolve, reject) => {
                reader.onload = function (e) {
                    resolve(e.target.result);
                };
                reader.onerror = reject;
                reader.readAsDataURL(photo);
    
            })
            let userPhoto = document.createElement("img");
            userPhoto.classList.add("message", "user-message"); // Можно стилизовать
            userPhoto.setAttribute('src', photo_base64);
            chatPlace.appendChild(userPhoto);
        };
        
        chatPlace.scrollTop = chatPlace.scrollHeight;
    }
    try {
        formData = new FormData(); // Создаем объект FormData
        formData.append("text", text);
        formData.append("gpt", selectedGPT);

        if (!generate_img_mode) {
            if (dataUploaded) {
                formData.append("photo", photo);
            }
        }else{
            formData.append("generate_img_mode", generate_img_mode);
        }

        let response = await fetch("/send", {
            method: "POST",
            body: formData
        });
        let result = await response.json();
        // Вернуть кнопку в исходное состояние
        sendButton.innerHTML = '<i class="h1 bi bi-send"></i>';
        sendButton.disabled = false;


        if (result.status === 'success') {
            document.getElementById("floatingTextarea").value = ""; // Очистка поля

            if (!generate_img_mode) {
                let botMessage = document.createElement("div");
                botMessage.classList.add("message", "bot-message");
                botMessage.textContent = result.message;
                chatPlace.appendChild(botMessage);
            }else{
                let botMessage = document.createElement("img");
                botMessage.classList.add("message", "bot-message");
                botMessage.setAttribute('src', result.message);
                chatPlace.appendChild(botMessage);
            }
        
            chatPlace.scrollTop = chatPlace.scrollHeight;

            let icon = document.getElementById("upload-img");
            icon.classList.remove("bi-check");
            icon.classList.add("bi-image"); 
            document.getElementById("fileInput").disabled = false;
            document.getElementById("custom-file-label").setAttribute("data-uploaded", "false");

            if (isAuthenticated){
                const chatElement = document.getElementById('chat-place');
                const model = document.getElementById('gpt_value').value;
                const user_message = text;
                const bot_message = botMessage.textContent;

                if (chatElement.childElementCount == 2 && chatElement.getElementsByClassName('bot-message')) {
                    let response = await fetch("/gpt/create_chat", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({"model": model, "user_message": user_message, "bot_message": bot_message })
                    });
                
                    let result = await response.json();
                    window.location.href = '/gpt/'+result.chat_id;

                }else{
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

document.getElementById('fileInput').addEventListener('change', async function () {
    const MAX_FILE_SIZE = 100 * 1024 * 1024; //100MB;
    let fileInput = this.files[0];
    
    if (!fileInput || !fileInput.type.startsWith("image/")) {
        alert("Выберите фото!");
        return;
    }

    if (fileInput.size > MAX_FILE_SIZE) {
        alert("Файл слишком большой. Максимальный размер: "+ Math.ceil(MAX_FILE_SIZE/(1024**2))+"MB");
        return;
    }

    // let reader = new FileReader();
    // reader.onload = function (e) {
    //     localStorage.setItem('savedFile', e.target.result); // Сохраняем base64 строку
    //     console.log("Файл сохранён в локальном хранилище!");
    // };

    // reader.readAsDataURL(fileInput); // Преобразуем файл в base64

    document.getElementById("fileInput").disabled = true;
    let icon = document.getElementById("upload-img");
    icon.classList.remove("bi-image"); 
    icon.classList.add("bi-check");
    document.getElementById("custom-file-label").setAttribute("data-uploaded", "true");

});

document.getElementById('enable-img-mode').addEventListener('change', function() {
    if (this.checked) {
        console.log('Переключатель ВКЛЮЧЕН');
        document.getElementById('custom-file-label').hidden = true
    } else {
        console.log('Переключатель ВЫКЛЮЧЕН');
        document.getElementById('custom-file-label').hidden = false
    }
});
