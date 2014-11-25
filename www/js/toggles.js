$('.toggle').each(function() {
  $(this).toggles({
    click: !$(this).hasClass('noclick'),
    drag: !$(this).hasClass('nodrag'),
    clicker: ($(this).attr('rel')) ? $('.'+$(this).attr('rel')) : null,
    on: $(this).hasClass('on'),
    checkbox: ($(this).data('checkbox')) ? $('.'+$(this).data('checkbox')) : null,
    text: {
      on: $(this).data('ontext') || 'ON',
      off: $(this).data('offtext') || 'OFF'
    },
    transition: 'ease-out',
    type: $(this).data('type')
  });
});

$('#theme').on('change',function() {
  $('.examples').removeClass('toggle-light toggle-dark toggle-iphone toggle-modern toggle-soft').addClass('toggle-'+$(this).find('option:selected').attr('rel'));
  _gs('event','Changed Theme to ' + $(this).find('option:selected').text());
});

$('.downloads .min').on('click',function() {
  _gs('event', 'Downloaded Toggles');
});
$('.downloads .minny').on('click',function() {
  _gs('event', 'Downloaded Minified Toggles');
});
