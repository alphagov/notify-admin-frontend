import { isSupported } from 'govuk-frontend';

// This new way of writing Javascript components is based on the GOV.UK Frontend skeleton Javascript coding standard
// that uses ES2015 Classes -
// https://github.com/alphagov/govuk-frontend/blob/main/docs/contributing/coding-standards/js.md#skeleton
//
// It replaces the previously used way of setting methods on the component's `prototype`.
// We use a class declaration way of defining classes -
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/class
//
// More on ES2015 Classes at https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes

class UpdateStatus {
  constructor($module) {
    if (!isSupported()) {
      return this;
    }

    const getRenderer = $component => response => $component.html(
      response.html
    );

    const throttle = (func, limit) => {

      let throttleOn = false;
      let callsHaveBeenThrottled = false;
      let timeout;

      return function() {

        const args = arguments;
        const context = this;

        if (throttleOn) {
          callsHaveBeenThrottled = true;
        } else {
          func.apply(context, args);
          throttleOn = true;
        }

        clearTimeout(timeout);

        timeout = setTimeout(() => {
          throttleOn = false;
          if (callsHaveBeenThrottled) func.apply(context, args);
          callsHaveBeenThrottled = false;
        }, limit);

      };

    };

    let id = 'update-status';

    this.$module = $module;
    this.$textbox = $('#' + this.$module.data('target'));

    this.$module
      .attr('id', id);

    this.$textbox
      .attr(
        'aria-describedby',
        (
          this.$textbox.attr('aria-describedby') || ''
        ) + (
          this.$textbox.attr('aria-describedby') ? ' ' : ''
        ) + id
      )
      .on('input', throttle(this.update, 150))
      .trigger('input');
        
  }

  update () {

    $.ajax(
      this.$module.data('updates-url'),
      {
        'method': 'post',
        'data': this.$textbox.parents('form').serialize()
      }
    ).done(
      getRenderer(this.$module)
    ).fail(
      () => {}
    );

  };
}

export default UpdateStatus;
