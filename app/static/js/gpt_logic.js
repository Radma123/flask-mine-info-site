document.getElementById("sendButton").addEventListener("click", async function() {
    let text = document.getElementById("floatingTextarea").value;
    let sendButton = document.getElementById("sendButton");
    let selectedGPT = document.getElementById("gpt_value").value;

    if (!text.trim()) return; // Игнорируем пустой ввод

    // Заменяем иконку отправки на спиннер
    sendButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    sendButton.disabled = true;

    // Отправка данных на сервер
    let response = await fetch("/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text, gpt: selectedGPT })
    });

    let result = await response.json();
    console.log(result)
    
    // Вернуть кнопку в исходное состояние
    sendButton.innerHTML = '<i class="h1 bi bi-send"></i>';
    sendButton.disabled = false;
    
    if (result.status === 'success') {
        document.getElementById("floatingTextarea").value = ""; // Очистка поля
        console.log(1)
    } else {
        alert("Ошибка при отправке: " + result.message);
        console.log(2)
    }
});
