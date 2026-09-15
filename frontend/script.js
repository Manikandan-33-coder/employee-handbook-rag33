// =========================================================
// FastAPI Backend URL
// =========================================================

const API_URL ="http://127.0.0.1:8000/ask";


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


// =========================================================
// Add Message to Chat
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
        message;


    messageWrapper.appendChild(
        messageContent
    );


    chatMessages.appendChild(
        messageWrapper
    );


    // Scroll to latest message
    setTimeout(() => {

        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    }, 50);
}


// =========================================================
// Show Loading
// =========================================================

function showLoading() {

    loading.classList.remove(
        "hidden"
    );

    askButton.disabled =
        true;

    questionInput.disabled =
        true;
}


// =========================================================
// Hide Loading
// =========================================================

function hideLoading() {

    loading.classList.add(
        "hidden"
    );

    askButton.disabled =
        false;

    questionInput.disabled =
        false;

    questionInput.focus();
}


// =========================================================
// Send Question to FastAPI
// =========================================================

async function askQuestion(question) {

    try {

        // Show loading
        showLoading();


        // Display user question
        addMessage(
            question,
            "user"
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

                    body:
                        JSON.stringify({
                            question:
                                question
                        })
                }
            );


        // =====================================================
        // Handle HTTP Error
        // =====================================================

        if (!response.ok) {

            let errorMessage =
                `Server error: ${response.status}`;


            try {

                const errorData =
                    await response.json();


                if (errorData.detail) {

                    errorMessage =
                        errorData.detail;

                }

            } catch (error) {

                console.error(
                    "Could not read error response:",
                    error
                );

            }


            throw new Error(
                errorMessage
            );
        }


        // =====================================================
        // Read JSON Response
        // =====================================================

        const data =
            await response.json();


        // =====================================================
        // Check AI Answer
        // =====================================================

        if (
            data.answer === undefined ||
            data.answer === null
        ) {

            throw new Error(
                "The backend did not return an answer."
            );

        }


        // =====================================================
        // Display AI Response
        // =====================================================

        addMessage(
            data.answer,
            "assistant"
        );


    } catch (error) {

        console.error(
            "API Error:",
            error
        );


        // Display error in chatbot
        addMessage(

            `Sorry, something went wrong: ${error.message}`,

            "assistant"

        );

    } finally {

        // Hide loading
        hideLoading();

    }
}


// =========================================================
// Form Submit
// =========================================================

if (questionForm) {

    questionForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const question =
                questionInput.value.trim();


            // Ignore empty questions
            if (!question) {

                return;

            }


            // Clear input
            questionInput.value =
                "";


            // Ask AI
            await askQuestion(
                question
            );

        }
    );

}


// =========================================================
// Clear Chat
// =========================================================

if (clearChatButton) {

    clearChatButton.addEventListener(
        "click",
        function() {

            // Remove all messages
            chatMessages.innerHTML =
                "";


            // Clear input
            questionInput.value =
                "";


            // Show welcome screen again
            const welcome =
                document.getElementById(
                    "welcome"
                );


            if (welcome) {

                welcome.style.display =
                    "block";

            }


            // Make sure loading is hidden
            loading.classList.add(
                "hidden"
            );


            // Enable controls
            askButton.disabled =
                false;

            questionInput.disabled =
                false;


            // Focus input
            questionInput.focus();

        }
    );

}


// =========================================================
// Enter Key Support
// =========================================================

if (questionInput) {

    questionInput.addEventListener(
        "keydown",
        function(event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                questionForm.requestSubmit();

            }

        }
    );

}


// =========================================================
// Initial Focus
// =========================================================

window.addEventListener(
    "load",
    function() {

        if (questionInput) {

            questionInput.focus();

        }

    }
);
