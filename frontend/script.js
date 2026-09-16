
// =========================================================
// Employee Handbook AI - Frontend
// =========================================================


// =========================================================
// Backend API
// =========================================================

const API_URL =
    "https://employee-handbook-rag33-6.onrender.com/ask";


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

const welcome =
    document.getElementById("welcome");


// =========================================================
// Check Elements
// =========================================================

console.log("========================================");
console.log("Employee Handbook AI loaded");
console.log("API:", API_URL);
console.log("Form:", questionForm);
console.log("Input:", questionInput);
console.log("Button:", askButton);
console.log("Messages:", chatMessages);
console.log("Loading:", loading);
console.log("========================================");


// =========================================================
// Validate Required Elements
// =========================================================

if (!questionForm) {
    console.error("ERROR: questionForm not found.");
}

if (!questionInput) {
    console.error("ERROR: questionInput not found.");
}

if (!askButton) {
    console.error("ERROR: askButton not found.");
}

if (!chatMessages) {
    console.error("ERROR: chatMessages not found.");
}

if (!loading) {
    console.error("ERROR: loading not found.");
}


// =========================================================
// Add Message
// =========================================================

function addMessage(message, sender) {

    if (!chatMessages) {
        return;
    }

    const messageText =
        String(message ?? "").trim();

    if (!messageText) {
        return;
    }


    // Create message wrapper
    const messageWrapper =
        document.createElement("div");

    messageWrapper.className =
        `message ${sender}`;


    // Create message content
    const messageContent =
        document.createElement("div");

    messageContent.className =
        "message-content";


    // Set message
    messageContent.textContent =
        messageText;


    // Add content to wrapper
    messageWrapper.appendChild(
        messageContent
    );


    // Add message to chat
    chatMessages.appendChild(
        messageWrapper
    );


    // Hide welcome screen after first message
    if (welcome) {
        welcome.style.display = "none";
    }


    // Scroll to latest message
    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// =========================================================
// Show Loading
// =========================================================

function showLoading() {

    if (loading) {
        loading.classList.remove("hidden");
    }

    if (askButton) {
        askButton.disabled = true;
    }

    if (questionInput) {
        questionInput.disabled = true;
    }
}


// =========================================================
// Hide Loading
// =========================================================

function hideLoading() {

    if (loading) {
        loading.classList.add("hidden");
    }

    if (askButton) {
        askButton.disabled = false;
    }

    if (questionInput) {
        questionInput.disabled = false;
        questionInput.focus();
    }
}


// =========================================================
// Ask Backend
// =========================================================

async function askQuestion(question) {

    const cleanQuestion =
        String(question ?? "").trim();


    // Do nothing for empty question
    if (!cleanQuestion) {
        return;
    }


    // -----------------------------------------------------
    // Show user message FIRST
    // -----------------------------------------------------

    addMessage(
        cleanQuestion,
        "user"
    );


    // Clear input
    if (questionInput) {
        questionInput.value = "";
    }


    // Show loading
    showLoading();


    try {

        console.log(
            "Sending request to:",
            API_URL
        );

        console.log(
            "Question:",
            cleanQuestion
        );


        // -------------------------------------------------
        // Call FastAPI
        // -------------------------------------------------

        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Accept":
                            "application/json",

                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question:
                            cleanQuestion
                    })
                }
            );


        console.log(
            "Backend status:",
            response.status
        );


        // -------------------------------------------------
        // Read response
        // -------------------------------------------------

        const data =
            await response.json()
                .catch(() => null);


        console.log(
            "Backend response:",
            data
        );


        // -------------------------------------------------
        // Handle HTTP errors
        // -------------------------------------------------

        if (!response.ok) {

            const errorMessage =
                data?.detail ||
                `Server error: ${response.status}`;

            throw new Error(
                errorMessage
            );
        }


        // -------------------------------------------------
        // Validate response
        // -------------------------------------------------

        if (
            !data ||
            typeof data.answer !== "string"
        ) {

            throw new Error(
                "Invalid response from backend."
            );
        }


        // -------------------------------------------------
        // Display AI answer
        // -------------------------------------------------

        addMessage(
            data.answer,
            "assistant"
        );


    } catch (error) {

        console.error(
            "API Error:",
            error
        );


        // Show useful error in chat
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

            event.stopPropagation();


            const question =
                questionInput.value.trim();


            if (!question) {

                questionInput.focus();

                return;
            }


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

            // Enter without Shift
            if (
                event.key === "Enter" &&
                !event.shiftKey
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
// Clear Chat
// =========================================================

if (clearChatButton) {

    clearChatButton.addEventListener(
        "click",
        function() {

            if (chatMessages) {
                chatMessages.innerHTML = "";
            }


            if (welcome) {
                welcome.style.display = "";
            }


            if (questionInput) {

                questionInput.value = "";

                questionInput.disabled = false;

                questionInput.focus();
            }


            if (askButton) {
                askButton.disabled = false;
            }

        }
    );
}


// =========================================================
// Initial State
// =========================================================

window.addEventListener(
    "load",
    function() {

        console.log(
            "Frontend initialization complete."
        );


        if (questionInput) {

            questionInput.disabled = false;

            questionInput.readOnly = false;

            questionInput.focus();
        }


        if (askButton) {
            askButton.disabled = false;
        }

    }
);

