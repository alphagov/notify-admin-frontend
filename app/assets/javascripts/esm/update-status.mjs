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

    

    const id = 'update-status';
    this.$module = $module;
    this.$textbox = document.querySelector(`#${this.$module.dataset.target}`);

    this.$module.setAttribute('id', id);

    this.$textbox.setAttribute( 'aria-describedby',
      (
        this.$textbox.getAttribute('aria-describedby') || ''
      ) + (
        this.$textbox.getAttribute('aria-describedby') ? ' ' : ''
      ) + id
    );
    this.$textbox.addEventListener("input", () => {
      this.throttle(this.update(), 150)
    });
        
  }

  async update () {
    await fetch(this.$module.dataset.updatesUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams(new FormData(this.getParent(this.$textbox, 'form'))).toString()
    })
    .then(res => res.json())
    .then((data) => {
      this.getRenderer(this.$module, data)
    })
    .catch(() => {
      () => {}
    });
  };

  getRenderer ($module, response) {
    $module.innerHTML = response.html
  }

  throttle (func, limit) {

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

  // instead of doing just document.querySelector
  // we use this to look up from the $module
  getParent(el, selector) {
    const parents= [];
    while ((el = el.parentNode) && el !== document) {
      if (!selector || el.matches(selector)) parents.push(el);
    }
    return parents[0];
  }
}

export default UpdateStatus;
