javascript
// =========================================================
// FastAPI Backend URL
// =========================================================

// Local development
const API_URL =
    "https://employee-handbook-rag33-4.onrender.com/ask";


// =========================================================
// Get HTML Elements
// =========================================================

const questionForm =
    document.getElementById("questionForm");

const questionInput =
    document.getElementById("questionInput");

const askButton =
    document.getElementById("askButton");

const chatMessages =
    document.getElementById("chatMessages");

const loading =
    document.getElementById("loading");

const clearChatButton =
    document.getElementById("clearChat");


// IMPORTANT:
// HTML uses class="quick-card"
const quickCards =
    document.querySelectorAll(".quick-card");


// =========================================================
// Check Elements
// =========================================================

console.log("Employee Handbook AI loaded.");

console.log(
    "Question input:",
    questionInput
);

console.log(
    "Question form:",
    questionForm
);

console.log(
    "Quick cards:",
    quickCards
);


// =========================================================
// Add Message
// =========================================================

function addMessage(message, sender) {

    const messageWrapper =
        document.createElement("div");

    messageWrapper.classList.add(
        "message",
        sender
    );


    const messageContent =
        document.createElement("div");

    messageContent.classList.add(
        "message-content"
    );


    messageContent.textContent =
        String(message ?? "");


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


    quickCards.forEach(
        card => {
            card.disabled = true;
        }
    );
}


// =========================================================
// Hide Loading
// =========================================================

function hideLoading() {

    loading.classList.add("hidden");

    askButton.disabled = false;

    questionInput.disabled = false;


    quickCards.forEach(
        card => {
            card.disabled = false;
        }
    );


    questionInput.focus();
}


// =========================================================
// Send Question to FastAPI
// =========================================================

async function askQuestion(question) {

    const cleanQuestion =
        String(question).trim();


    if (!cleanQuestion) {
        return;
    }


    try {

        // Display user question
        addMessage(
            cleanQuestion,
            "user"
        );


        // Show loading
        showLoading();


        console.log(
            "Sending question:",
            cleanQuestion
        );


        // Send request to FastAPI
        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question:
                            cleanQuestion
                    })
                }
            );


        // Read response
        const data =
            await response
                .json()
                .catch(() => null);


        // Handle HTTP errors
        if (!response.ok) {

            throw new Error(
                data?.detail ||
                `Server error: ${response.status}`
            );
        }


        // Validate answer
        if (
            !data ||
            typeof data.answer !== "string"
        ) {

            throw new Error(
                "Invalid response from backend."
            );
        }


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

if (
    questionForm &&
    questionInput
) {

    questionForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const question =
                questionInput.value.trim();


            if (!question) {

                questionInput.focus();

                return;
            }


            // Clear input
            questionInput.value = "";


            // Ask question
            await askQuestion(
                question
            );
        }
    );
}


// =========================================================
// Enter Key
// =========================================================

if (questionInput) {

    questionInput.addEventListener(
        "keydown",
        function(event) {

            if (
                event.key === "Enter"
            ) {

                event.preventDefault();


                if (
                    questionInput.value.trim()
                ) {

                    questionForm.requestSubmit();
                }
            }
        }
    );
}


// =========================================================
// Quick Question Cards
// =========================================================

quickCards.forEach(
    card => {

        card.addEventListener(
            "click",
            async function() {

                const question =
                    card.dataset.question;


                if (!question) {
                    return;
                }


                // Put question into input
                questionInput.value =
                    question;


                // Send question
                await askQuestion(
                    question
                );


                // Clear input after sending
                questionInput.value = "";

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
        function() {

            chatMessages.innerHTML = "";

            questionInput.value = "";

            questionInput.disabled = false;

            askButton.disabled = false;

            questionInput.focus();

        }
    );
}


// =========================================================
// Initial State
// =========================================================

window.addEventListener(
    "load",
    function() {

        if (questionInput) {

            questionInput.disabled = false;

            askButton.disabled = false;

            questionInput.focus();
        }
    }
);

