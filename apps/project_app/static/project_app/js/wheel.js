var count = $(".triangle").length;
var spin = function(index) {
  var $spinner = $(".spinner");

  var value = index >= 0 ? index : parseInt(Math.random() * count);

  var preffix = "index-";

  $spinner.toggleClass("spin");
  $spinner[0].className = $spinner[0].className.replace(
    new RegExp("(^|\\s)" + preffix + "\\S+", "g"),
    ""
  );
  $spinner.addClass(preffix + value);
};

