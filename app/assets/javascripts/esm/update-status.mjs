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
      // console.log(el)
      // this.$textbox.dispatchEvent(new Event("input"))
      throttle(this.update(), 150)
      // el.dispatchEvent(new Event('input', { bubbles: true }));
    });
        
  }

  async update () {
    console.log('tostring', new URLSearchParams(new FormData(this.getParent(this.$textbox, 'form'))).toString())
    console.log('stringify', JSON.stringify(new URLSearchParams(new FormData(this.getParent(this.$textbox, 'form'))).toString()))
    console.log('random', new URLSearchParams(new FormData(this.getParent(this.$textbox, 'form'))).toString())
    await fetch(this.$module.dataset.updatesUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: new URLSearchParams(new FormData(this.getParent(this.$textbox, 'form'))).toString()
    })
    .then(res => res.json())
    .then((data) => {
      console.log('response', data)
      this.getRenderer(this.$module, data)
    })
    .catch(() => {
      () => {}
    });

    // $.ajax(
    //   this.$module.dataset.updatesUrl,
    //   {
    //     'method': 'post',
    //     'data': new URLSearchParams(new FormData(this.$textbox.parentNode('form'))).toString();
    //   }
    // ).done(
    //   this.getRenderer(this.$module)
    // ).fail(
    //   () => {}
    // );

  };

  getRenderer ($module, response) {
    $module.innerHTML = response.html
  }

  getParent(el, selector) {
    const parents= [];
    while ((el = el.parentNode) && el !== document) {
      if (!selector || el.matches(selector)) parents.push(el);
    }
    return parents[0];
  }
}

export default UpdateStatus;
