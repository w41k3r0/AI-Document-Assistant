const uploadForm = document.getElementById("upload-form");
const uploadButton = document.getElementById("upload-button");
const pdfFiles = document.getElementById("pdf-files");
const uploadStatus = document.getElementById("upload-status");
const documentList = document.getElementById("document-list");
const questionForm =  document.getElementById("question-form");
const questionInput = document.getElementById("question");
const questionStatus = document.getElementById("question-status");
const askButton = document.getElementById("ask-button");
const chatMessages = document.getElementById("chat-messages");

pdfFiles.addEventListener("change", () => {
    const fileCount = pdfFiles.files.length;
    uploadButton.disabled = fileCount === 0;
})

uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    
    if (pdfFiles.files.length === 0) {
        uploadStatus.textContent = "Please select PDF files.";
        return;
    }
    if (pdfFiles.files.length > 5) {
        uploadStatus.textContent = "Upload at most 5 PDFs at a time.";
        return;
    }

    const formData = new FormData(uploadForm)
    uploadButton.disabled = true;
    pdfFiles.disabled = true;
    uploadStatus.textContent = "Uploading and processing your PDFs...";

    try {
        const response = await fetch(uploadForm.action, {
            method : "POST",
            body : formData,
        });

        const data = await response.json()

        if (!response.ok) {
            throw new Error(
                data.error || "The upload failed. Please try again."
            );
        }
        uploadStatus.textContent = data.message;
        renderDocuments(data.documents);
        chatMessages.replaceChildren();
        questionInput.value = "";
        questionStatus.textContent = "";
        questionInput.disabled = false;
        askButton.disabled = false;
        questionInput.focus();
    
    } catch (error) {
        uploadStatus.textContent = error.message;
    
    } finally {
        pdfFiles.disabled = false;
        uploadButton.disabled = pdfFiles.files.length === 0;
    }

})

function renderDocuments(documents) {
    documentList.replaceChildren();

    for (const doc of documents) {
        const item = document.createElement("li");
        item.className = "flex min-w-0 items-center gap-3 rounded-2xl border border-white/10 bg-neutral-900 px-4 py-3";

        const badge = document.createElement("span");
        badge.className = "flex h-11 w-10 shrink-0 items-center justify-center rounded-lg border border-neutral-700 bg-neutral-800 text-[10px] font-semibold tracking-wide text-neutral-300";
        badge.textContent = "PDF";

        const info = document.createElement("div");
        info.className = "min-w-0 flex-1";

        const fileName = document.createElement("p");
        fileName.className = "truncate text-sm font-medium text-neutral-100";
        fileName.textContent = doc.source;
        fileName.title = doc.source;

        const status = document.createElement("p");
        status.className = "mt-1 text-xs text-neutral-400";
        status.textContent = "Ready to ask";

        item.append(badge, info);
        info.append(fileName, status);
        documentList.append(item);

    }
}

questionForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (askButton.disabled || pdfFiles.disabled) {
        return;

    }
    const question = questionInput.value.trim();
    if (!question) {
        questionStatus.textContent = "Please enter a question.";
        return;
    }

    questionInput.disabled = true;
    askButton.disabled = true;
    pdfFiles.disabled = true;
    uploadButton.disabled = true;

    showQuestionLoading();

    try {
        const response = await fetch(questionForm.action, {
            method : "POST",
            headers : {
                "Content-Type" : "application/json",
            },
            body : JSON.stringify({
                question : question,
            }),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(
                data.error || "The answer could not be generated."
            );
        }
        const emptyState = document.getElementById("empty-state");
        if (emptyState) {
            emptyState.remove();
        }

        addMessage("You", question);
        const assistantMessage = addMessage("Assistant", data.answer);
        renderSources(data.sources, assistantMessage);
        scrollToMessage(assistantMessage);

        questionInput.value = "";
        questionStatus.textContent = "";

    } catch (error) {
        questionStatus.textContent = error.message;
    } finally {
        questionInput.disabled = false;
        askButton.disabled = false;
        pdfFiles.disabled = false;
        uploadButton.disabled = pdfFiles.files.length === 0;

        questionInput.focus({ preventScroll : true });

    }

});

function addMessage(label, text) {
    const message = document.createElement("div");
    const isUser = label === "You";
    
    if (isUser) {
        message.className = "ml-auto max-w-[85%] rounded-2xl bg-neutral-800 px-4 py-3";
    } else {
        message.className = "w-full scroll-mt-6 py-4";
    }

    const heading = document.createElement("p");
    heading.textContent = label;

    if (isUser) {
        heading.className = "sr-only";
    } else {
        heading.className = "mb-3 text-xs font-medium tracking-wide text-neutral-400";
    }

    const content = document.createElement("div");

    if (isUser) {
        content.className = "whitespace-pre-wrap break-words text-sm leading-7 text-neutral-100";
        content.textContent = text;
    } else {
        content.className = "markdown-content min-w-0 text-sm leading-7 text-neutral-100";
        
        const html = marked.parse(text);
        const cleanHtml = DOMPurify.sanitize(html, {
            ALLOWED_TAGS : [
                "p", "br", "strong", "em", "del", "h1", "h2", "h3", "h4", "h5", "h6", "ul",
                "ol", "li", "blockquote", "pre", "code", "hr", "table", "thead", "tbody", "tr",
                "th", "td"
            ],
            ALLOWED_ATTR : ["start", "colspan", "rowspan"],
            ALLOW_DATA_ATTR : false,
            ALLOW_ARIA_ATTR : false,

        });
        content.innerHTML = cleanHtml;

    }

    message.append(heading, content);
    chatMessages.append(message);

    return message;
    
}

function renderSources(sources, messageElement) {
    if (sources.length === 0) {
        return;
    }

    const sourceSection = document.createElement("div");
    sourceSection.className = "mt-4 border-t border-neutral-800 pt-4";

    const heading = document.createElement("h3");
    heading.className = "mb-3 text-xs font-medium text-neutral-400";
    heading.textContent = "Sources";

    sourceSection.append(heading);

    for (const source of sources) {
        const details = document.createElement("details");
        details.className = "mt-2 rounded-xl border border-neutral-800 bg-neutral-950/50 p-3";

        const summary = document.createElement("summary");
        summary.className = "cursor-pointer break-words text-sm text-neutral-200";
        summary.textContent = `[${source.label}] ${source.source} | Page ${source.page}`;

        const passage = document.createElement("p");
        passage.className = "mt-3 whitespace-pre-wrap break-words text-sm leading-6 text-neutral-400";
        passage.textContent = source.text;

        details.append(summary, passage);
        sourceSection.append(details);

    }
    messageElement.append(sourceSection);

}

function showQuestionLoading() {
    const spinner = document.createElement("span");
    spinner.className = "inline-block h-4 w-4 shrink-0 rounded-full border-neutral-600 border-t-neutral-100 motion-safe:animate-spin";
    spinner.setAttribute("aria-hidden", "true");

    const label = document.createElement("span");
    label.textContent = "Finding an answer...";

    questionStatus.className = "mt-3 flex items-center gap-2 text-sm text-neutral-300";
    questionStatus.replaceChildren(spinner, label);
}

function scrollToMessage(messageElement) {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    messageElement.scrollIntoView({
        behavior : reduceMotion ? "instant" : "smooth",
        block : "start",

    });
}
