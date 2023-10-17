function applyLoadingAnimation() {
  const styleElement = document.createElement("style");
  styleElement.textContent = `
    .loading-animation {
      margin: 10px;
      margin-right: auto;
    }

    .loading-animation span {
      width: 10px;
      height: 10px;
      background-color: #e0e0e0;
      display: inline-block;
      margin: 1px;
      border-radius: 50%;
    }

    .loading-animation span:nth-child(1) {
      animation: bounce 1s infinite;
    }

    .loading-animation span:nth-child(2) {
      animation: bounce 1s infinite 0.2s;
    }

    .loading-animation span:nth-child(3) {
      animation: bounce 1s infinite 0.4s;
    }
    
    @keyframes bounce {
      0% {
        transform: translateY(0px);
      }
      40% {
        transform: translateY(8px);
      }
      80% {
        transform: translateY(0px);
      }
    }
  `;

  document.head.appendChild(styleElement);
}

function removeLoadingAnimation() {
  const styleElement = document.querySelector("style");
  if (styleElement) {
    styleElement.remove();
  }
}

class Chatbox {
  constructor() {
    this.args = {
      // openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
    };

    // this.state = false;
    this.messages = [];
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;

    // openButton.addEventListener("click", () => this.toggleState(chatBox));

    sendButton.addEventListener("click", () => this.onSendButton(chatBox));

    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendButton(chatBox);
      }
    });
  }

  // toggleState(chatbox) {
  //   this.state = !this.state;

  //   // show or hide the box
  //   if (this.state) {
  //     chatbox.classList.add("chatbox--active");
  //   } else {
  //     chatbox.classList.remove("chatbox--active");
  //   }
  // }

  onSendButton(chatbox) {
    var textField = chatbox.querySelector("input");
    let text1 = textField.value;
    if (text1 === "") {
      return;
    }

    let msg1 = { name: "User", message: text1 };
    this.messages.push(msg1);
    this.updateChatText(chatbox);
    textField.value = "";

    // Add typing indicator message with animation
    // let typingMsg = { name: "Pi", message: "Typing" };
    // this.messages.push(typingMsg);
    // this.updateChatText(chatbox);

    // Simulate typing animation
    applyLoadingAnimation();

    setTimeout(() => {
      fetch($SCRIPT_ROOT + "/predict", {
        method: "POST",
        body: JSON.stringify({ message: text1 }),
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((r) => r.json())
        .then((r) => {
          // Remove the typing indicator message
          // this.messages.pop();
          removeLoadingAnimation();

          let msg2 = { name: "Pi", message: r.answer };
          this.messages.push(msg2);
          this.updateChatText(chatbox);
          textField.value = "";
        })
        .catch((error) => {
          removeLoadingAnimation();
          console.error("Error: ", error);
          this.updateChatText(chatbox);
          textField.value = "";
        });
    }, 1000); // Adjust the timeout duration as needed
  }

  updateChatText(chatbox) {
    var html = "";
    this.messages
      .slice()
      .reverse()
      .forEach(function (item) {
        if (item.name == "Pi") {
          html +=
            '<div class="messages__item messages__item--visitor">' +
            item.message +
            "</div>";
        } else {
          html +=
            '<div class="messages__item messages__item--operator">' +
            item.message +
            "</div>";
        }
      });

    const chatMessage = chatbox.querySelector(".chatbox__messages");
    chatMessage.innerHTML = html;
  }
}

const chatbox = new Chatbox();
chatbox.display();
