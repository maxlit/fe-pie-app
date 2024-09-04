$(document).ready(function() {
    $("#search-form button").click(function(event) {
      event.preventDefault();
  
      var lang = $("#lang-select").val();
      var term = $("#search-term").val();
      var proto_lang = $(this).val();
  
      if ($(this).attr("id") === "search-btn") {
        console.log("Search button clicked");
        if (proto_lang === "tinder") {
          window.location.href = "/" + proto_lang + "/s?l=" + lang + "&w=" + term;
        } else {
          window.location.href = "/" + proto_lang + "/search?l=" + lang + "&w=" + term;
        }
      } else if ($(this).attr("id") === "random-btn") {
        if (proto_lang === "tinder") {
          window.location.href = "/" + proto_lang + "/r?l=" + lang;
        } else {
          window.location.href = "/" + proto_lang + "/random?l=" + lang;
        }
      }
    });

    const suggestionDropdown = $("#suggestion-dropdown");
    const endpoint = suggestionDropdown.data('api-endpoint');
    // Listen for input changes in the search box
    $("#search-term").on("input", function () {
      const input = $(this).val();
      const lang = $("#lang-select").val();

      // Only proceed if the input has more than 3 characters
      if (input.length >= 2) {
        // Make an AJAX request to the Flask API for suggestions
        $.ajax({
          type: "GET",
          url: endpoint,
          data: { term: input, lang: lang },
          success: function (response) {
            // Log the API response to the browser console
            console.log("API Response: ", response);

            // Clear previous suggestions
            suggestionDropdown.empty();

            // Add each suggestion as a new <li> in the <ul> list
            response.suggestions.forEach((suggestion) => {
              suggestionDropdown.append(
                "<a class='dropdown-item' href='#''>" + suggestion + "</a>"
              );
            });
          },
          error: function (error) {
            console.error("Error in AJAX request: ", error);
            $("#suggestion-dropdown").empty();
          },
        });
      } else {
        // Clear suggestions and hide the suggestion dropdown if input length is less than 3 characters
        //suggestionDropdown.find(".suggestion-item").remove();
      }
    });

    // Handle suggestion click
    $("#suggestion-dropdown").on("click", "a", function () {
      var suggestion = $(this).text();
      $("#search-term").val(suggestion);
      $("#suggestion-dropdown").empty();
      $("#search-btn").click();
    });
  });
  