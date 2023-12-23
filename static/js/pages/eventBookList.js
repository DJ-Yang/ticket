function getCoupon(couponNumber) {
  $.ajax({
    url: "/event/download/",
    method: "POST",
    data: {'couponNumber': couponNumber},
    headers: {
      "X-CSRFToken": csrftoken
    },
    success: function (result) {
      drawEventBookList()
    },
    error: function (error) {
      alert("Failed Coupon Download");
      console.log(error);
    }
  });
}

function drawEventBookList() {
  $('#event-book-list').off("click", "a.btn-primary");
  
  $.ajax({
    url: "/event/list",
    dataType : "json",
    success: function (result) {
      const eventBookList = result.map(item => cardComponent(item.book.title, item.quantity, item.received, item.number));
      $('#event-book-list').html(eventBookList);

      $('#event-book-list').on("click", "a.btn-primary", function () {
        const number = $(this).data('number');
        getCoupon(number);
      });
    },
    fail: function (error) {
      alert("Failed Get Event Book List");
    }
  })
}
