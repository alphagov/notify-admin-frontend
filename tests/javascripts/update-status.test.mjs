import UpdateStatus from '../../app/assets/javascripts/esm/update-status.mjs';
import * as helpers from './support/helpers.js';
import { jest } from '@jest/globals';

// const each = require('jest-each').default;


const serviceNumber = '6658542f-0cad-491f-bec8-ab8457700ead';
const updatesURL = `/services/${serviceNumber}/templates/count-sms-length`;

let responseObj = {};
let mockResponse;

beforeAll(() => {

  // ensure all timers go through Jest
  jest.useFakeTimers();

  // // mock the bits of jQuery used
  // jest.spyOn(window.$, 'ajax');

  jest.spyOn(global, 'fetch').mockResolvedValue({
    json: jest.fn().mockResolvedValue(mockResponse),
  });

  // // set up the object returned from $.ajax so it responds with whatever responseObj is set to
  // jqueryAJAXReturnObj = {
  //   done: callback => {
  //     // For these tests the server responds immediately
  //     callback(responseObj);
  //     return jqueryAJAXReturnObj;
  //   },
  //   fail: () => {}
  // };

  // $.ajax.mockImplementation(() => jqueryAJAXReturnObj);

});

describe('Update content', () => {

  beforeEach(() => {

    document.body.classList.add('govuk-frontend-supported')
    document.body.innerHTML = `
      <form>
        <input type="hidden" name="csrf_token" value="abc123" />
        <label for="template_content" id="template-content-label">Template content<label>
        <span id="example-hint-text">Example hint text</span>
        <textarea name="template_content" id="template_content" aria-describedby="example-hint-text">Content of message</textarea>
      </form>
      <div data-notify-module="update-status" data-updates-url="${updatesURL}" data-target="template_content">
        Initial content
      </div>
    `;

  });

  afterEach(() => {

    document.body.innerHTML = '';

    // tidy up record of mocked AJAX calls
    // $.ajax.mockClear();

    // // ensure any timers set by continually starting the module are cleared
    // jest.clearAllTimers();

  });

  test("It should add attributes to the elements", () => {

   new UpdateStatus(document.querySelector('[data-notify-module="update-status"]'));

    expect(
      document.querySelectorAll('[data-notify-module=update-status]')[0].id
    ).toEqual(
      "update-status"
    );

    expect(
      document.getElementById('template_content').getAttribute('aria-describedby')
    ).toEqual(
      "example-hint-text update-status"
    );

  });

  test("It should handle a textarea without an aria-describedby attribute", () => {

    document.getElementById('template_content').removeAttribute('aria-describedby');

   new UpdateStatus(document.querySelector('[data-notify-module="update-status"]'));

    expect(
      document.getElementById('template_content').getAttribute('aria-describedby')
    ).toEqual(
      "update-status"
    );

  });

  test.only("It should make requests to the URL specified in the data-updates-url attribute", () => {

   new UpdateStatus(document.querySelector('[data-notify-module="update-status"]'));

   expect(fetchMock).toHaveBeenCalledWith(updatesURL);

    expect($.ajax.mock.calls[0][0]).toEqual(updatesURL);
    expect($.ajax.mock.calls[0]).toEqual([
      updatesURL,
      {
        "body": "csrf_token=abc123&template_content=Content%20of%20message",
        "method": "post"
      }
    ]);

  });

  test("It should replace the content of the div with the returned HTML", () => {

    responseObj = {'html': 'Updated content'}

    expect(
      document.querySelectorAll('[data-notify-module=update-status]')[0].textContent.trim()
    ).toEqual(
      "Initial content"
    );

   new UpdateStatus(document.querySelector('[data-notify-module="update-status"]'));

    expect(
      document.querySelectorAll('[data-notify-module=update-status]')[0].textContent.trim()
    ).toEqual(
      "Updated content"
    );

  });

  test("It should fire when the content of the textarea changes", () => {

    let textarea = document.getElementById('template_content');

    // Initial update triggered
   new UpdateStatus(document.querySelector('[data-notify-module="update-status"]'));
    expect($.ajax.mock.calls.length).toEqual(1);

    // 150ms of inactivity
    jest.advanceTimersByTime(150);
    helpers.triggerEvent(textarea, 'input');

    expect($.ajax.mock.calls.length).toEqual(2);

  });

  test("It should fire only after 150ms of inactivity", () => {

    let textarea = document.getElementById('template_content');

    // Initial update triggered
   new UpdateStatus(document.querySelector('[data-notify-module="update-status"]'));
    expect($.ajax.mock.calls.length).toEqual(1);

    helpers.triggerEvent(textarea, 'input');
    jest.advanceTimersByTime(149);
    expect($.ajax.mock.calls.length).toEqual(1);

    helpers.triggerEvent(textarea, 'input');
    jest.advanceTimersByTime(149);
    expect($.ajax.mock.calls.length).toEqual(1);

    helpers.triggerEvent(textarea, 'input');
    jest.advanceTimersByTime(149);
    expect($.ajax.mock.calls.length).toEqual(1);

    // > 150ms of inactivity
    jest.advanceTimersByTime(1);
    expect($.ajax.mock.calls.length).toEqual(2);

  });

});
