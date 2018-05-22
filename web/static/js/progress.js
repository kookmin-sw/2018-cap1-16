 $(document).ready(function() {
      $('.progress-bar').css("height",
                function() {
                    return $(this).attr("aria-valuenow") + "%";
                }
        )
    });