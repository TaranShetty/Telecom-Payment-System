let chatbotInitialized = false;

function toggleChatbot(){
   const box = document.getElementById("chatbot-box");
   const messages = document.getElementById("chatbot-messages");

   box.classList.toggle("open");
   if(!chatbotInitialized && box.classList.contains("open")){
    messages.innerHTML +=`
    <div class ="bot-msg fade-in">
    Hi! I am your AI Assistant.<br><br>
                I can help you with:
                <ul>
                    <li>📊 Pending amounts (PGCIL, JIO, BSNL)</li>
                    <li>⏳ Pending quarters & BSNL half-year cycles</li>
                    <li>📈 Dashboard insights</li>
                    <li>📄 Excel / table data</li>
                </ul>
    </div>
   `;
   chatbotInitialized = true;
    messages.scrollTop = messages.scrollHeight;

    
   }
}
function sendMessage(){
  let input = document.getElementById("chatbot-text");
  let message = input.value.trim();
  if(message ==="") return;

  let box = document.getElementById("chatbot-messages");
  box.innerHTML += `<div class="user-msg">${message}</div>`;
  input.value ="";
  
    fetch("/chatbot",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message:message})
    })
    .then(response => response.json())
    .then(data => {
        box.innerHTML += `<div class="bot-msg">${data.reply}</div>`;
        box.scrollTop = box.scrollHeight;
    });
}