// =========================================================
// FastAPI Backend URL
// =========================================================

const API_URL = "http://127.0.0.1:8000/ask";


// =========================================================
// Get HTML Elements
// =========================================================

const questionForm = document.getElementById("questionForm");
const questionInput = document.getElementById("questionInput");
const askButton = document.getElementById("askButton");

const chatMessages = document.getElementById("chatMessages");
const loading = document.getElementById("loading");

const clearChatButton = document.getElementById("clearChat");

const suggestionCards = document.querySelectorAll(
    ".suggestion-card"
);


// =========================================================
// Add Message to Chat
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


    messageWrapper.appendChild(messageContent);

    chatMessages.appendChild(messageWrapper);


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

    // Disable suggestion cards while processing
    suggestionCards.forEach(
        card => card.disabled = true
    );
}


// =========================================================
// Hide Loading
// =========================================================

function hideLoading() {

    loading.classList.add("hidden");

    askButton.disabled = false;

    questionInput.disabled = false;

    // Enable suggestion cards
    suggestionCards.forEach(
        card => card.disabled = false
    );

    questionInput.focus();
}


// =========================================================
// Send Question to FastAPI
// =========================================================

async function askQuestion(question) {

    try {

        showLoading();


        // Display user question
        addMessage(
            question,
            "user"
        );


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


        // Handle HTTP errors
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


        // Read JSON response
        const data =
            await response.json();


        // Display AI response
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


        // Ignore empty questions
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
// Suggested Question Cards
// =========================================================

suggestionCards.forEach(
    card => {

        card.addEventListener(
            "click",
            async function () {

                const question =
                    card.dataset.question;


                if (!question) {
                    return;
                }


                // Put question into input
                questionInput.value =
                    question;


                // Clear input after selecting
                questionInput.value = "";


                // Send question
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
