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

document.getElementById("sendButton").addEventListener("click", async function() {
    // Сбор данных HTML______________________________________________________________________________________________________________
    let user_message = document.getElementById("floatingTextarea").value;
    let selectedGPT = document.getElementById("gpt_value").value;
    let dataUploaded = document.getElementById('custom-file-label').getAttribute('data-uploaded');
    let photo = null;
    let generate_img_mode = document.getElementById('custom-file-label').hidden;  // Булево значение
    let chat_id = window.location.pathname.split('/').filter(Boolean).pop()
    isAuthenticated;

    let chatPlace = document.querySelector(".chat-place");
    let sendButton = document.getElementById("sendButton");

    // Проверка на пустой ввод
    if (!user_message.trim()) return;

    // Меняем кнопку на спиннер перед отправкой
    sendButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    sendButton.disabled = true;

    // Если загружено изображение
    if (dataUploaded === 'true') {
        photo = document.getElementById('fileInput').files[0];
    }

    // Отображение сообщения пользователя______________________________________________________________________________________________________________
    if (generate_img_mode === false) { 
        let userMessage = document.createElement("div");
        userMessage.classList.add("message", "user-message");
        userMessage.textContent = user_message;
        chatPlace.appendChild(userMessage);
    } else {
        try {
            let reader = new FileReader();
            let photo_base64 = await new Promise((resolve, reject) => {
                reader.onload = (e) => resolve(e.target.result);
                reader.onerror = reject;
                reader.readAsDataURL(photo);
            });

            let userPhoto = document.createElement("img");
            userPhoto.classList.add("message", "user-message");
            userPhoto.setAttribute('src', photo_base64);
            chatPlace.appendChild(userPhoto);
        } catch (error) {
            console.error("Ошибка чтения файла:", error);
            return;
        }
    }

    // Прокрутка вниз
    chatPlace.scrollTop = chatPlace.scrollHeight;

    //Обработка и отправка сообщения______________________________________________________________________________________________________________
    formData = new FormData();
    formData.append("user_message", user_message);
    formData.append("gpt", selectedGPT);
    formData.append("photo", photo);
    formData.append("generate_img_mode", generate_img_mode);
    formData.append("chat_id", chat_id);
    
    if (!isAuthenticated) {
        formData.append("database_mode", "guest");
    }else if (chat_id != "gpt"){
        formData.append("database_mode", "add_to_chat");
    }else if (chatPlace.childElementCount == 1){
        formData.append("database_mode", "create_chat");
    }else{
        alert('Error of chosing your current status')
    }

    try{
        let response = await fetch("/send", {
            method: "POST",
            body: formData
        });
        let result = await response.json();

        if (result.status === 'success') {
            console.log(bot_url);
            if (result.bot_url != 'None') {
                let botMessage = document.createElement("img");
                botMessage.classList.add("message", "bot-message");
                botMessage.setAttribute('src', result.bot_url);
                chatPlace.appendChild(botMessage);
            }else{
                let botMessage = document.createElement("div");
                botMessage.classList.add("message", "bot-message");
                botMessage.textContent = result.message;
                chatPlace.appendChild(botMessage);
            }



            //очистка чата и файлов
            document.getElementById("floatingTextarea").value = "";
            let icon = document.getElementById("upload-img");
            icon.classList.remove("bi-check");
            icon.classList.add("bi-image"); 
            document.getElementById("fileInput").disabled = false;
            document.getElementById("custom-file-label").setAttribute("data-uploaded", "false");
            document.getElementById('fileInput').value = "";
        }else{
            alert("Ошибка при отправке (попробуйте выбрать другую модель): " + result.message);
        }
    }catch(err){
        console.error("Ошибка при отправке запроса:", err);
        alert("Ошибка сети. Проверьте соединение и попробуйте снова.");
    }finally{
        sendButton.innerHTML = '<i class="h1 bi bi-send"></i>';
        sendButton.disabled = false;
    }
    
});
