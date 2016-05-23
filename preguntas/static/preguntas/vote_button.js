var $voteButtons = $('.voteButton')
var $upButtons = $('.upButton')
var $downButtons = $('.downButton')
$upButtons.click(function(e){
    e.preventDefault();
    console.log('clicked');
    var scoreID = this.id.replace('-up','-score');
    if($( this ).hasClass('btn-success')){
      console.log('has btn-success');
      $( this ).removeClass('btn-success');
      $.ajax()
    } else {
      console.log('doesn\'t have btn-success');
      $( this ).addClass('btn-success');
    };
  });
