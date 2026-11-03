document
  .querySelectorAll("form[data-prevent-duplicate-submit]")
  .forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (form.dataset.submitting === "true") {
        event.preventDefault();
        return;
      }

      form.dataset.submitting = "true";
      const submitButton = form.querySelector('button[type="submit"]');
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent =
          submitButton.dataset.submittingLabel || submitButton.textContent;
      }
    });
  });
