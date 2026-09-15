```javascript
// =========================================================
// FastAPI Backend URL
// =========================================================

// Deployed Render backend
const API_URL = "https://employee-handbook-rag33-4.onrender.com/ask";


// =========================================================
// Get HTML Elements
// =========================================================

const questionForm = document.getElementById("questionForm");
const questionInput = document.getElementById("questionInput");
const askButton = document.getElementById("askButton");

const chatMessages = document.getElementById("chatMessages");
const loading = document.getElementById("loading");

const clearChatButton = document.getElementById("clearChat");

const quickCards = document.querySelectorAll(".quick-card");


// =========================================================
// Add Message
// =========================================================

function addMessage(message, sender) {

    const messageWrapper = document.createElement("div");

    messageWrapper.classList.add(
        "message",
        sender
    );

    const messageContent = document.createElement("div");

    messageContent.classList.add(
        "message-content"
    );

    messageContent.textContent = message;

    messageWrapper.appendChild(
        messageContent
    );

    chatMessages.appendChild(
        messageWrapper
    );

    // Scroll to latest message
    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// =========================================================
// Show Loading
// =========================================================

function showLoading() {

    loading.classList.remove("hidden");

    askButton.disabled = true;
    questionInput.disabled = true;

    quickCards.forEach(card => {
        card.disabled = true;
    });
}


// =========================================================
// Hide Loading
// =========================================================

function hideLoading() {

    loading.classList.add("hidden");

    askButton.disabled = false;
    questionInput.disabled = false;

    quickCards.forEach(card => {
        card.disabled = false;
    });

    questionInput.focus();
}


// =========================================================
// Ask Question
// =========================================================

async function askQuestion(question) {

    try {

        // Show user question
        addMessage(
            question,
            "user"
        );

        // Show loading
        showLoading();

        // Send request to FastAPI
        const response = await fetch(
            API_URL,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        // Check server response
        if (!response.ok) {

            const errorData =
                await response
                    .json()
                    .catch(() => null);

            throw new Error(
                errorData?.detail ||
                `Server error: ${response.status}`
            );
        }

        // Convert response to JSON
        const data =
            await response.json();

        // Show AI answer
        addMessage(
            data.answer,
            "assistant"
        );

    } catch (error) {

        console.error(
            "API Error:",
            error
        );

        addMessage(
            `Sorry, something went wrong: ${error.message}`,
            "assistant"
        );

    } finally {

        hideLoading();
    }
}


// =========================================================
// Form Submit
// =========================================================

questionForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const question =
            questionInput.value.trim();

        // Ignore empty input
        if (!question) {
            return;
        }

        // Clear input
        questionInput.value = "";

        // Ask question
        await askQuestion(question);
    }
);


// =========================================================
// Quick Action Cards
// =========================================================

quickCards.forEach(
    card => {

        card.addEventListener(
            "click",
            async function () {

                const question =
                    card.dataset.question;

                if (!question) {
                    return;
                }

                await askQuestion(
                    question
                );
            }
        );
    }
);


// =========================================================
// Clear Chat
// =========================================================

if (clearChatButton) {

    clearChatButton.addEventListener(
        "click",
        function () {

            chatMessages.innerHTML = "";

            questionInput.value = "";

            questionInput.focus();
        }
    );
}
```
