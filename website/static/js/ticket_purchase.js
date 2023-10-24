document.addEventListener("DOMContentLoaded", function () {
  // Check if the session variable 'ticketPurchaseSuccess' is set and is true
  const ticketPurchaseModal = new bootstrap.Modal(
    document.getElementById("ticketPurchaseModal")
  );

  // If the purchase was successful, show the modal
  if (ticketPurchaseSuccess) {
    console.log("Session variable 'ticketPurchaseSuccess' is set to true");
    // Display the ticket purchase modal
    ticketPurchaseModal.show();
  }
});
