import { createElement } from 'lwc';
import HelloWorld from 'c/helloWorld';

describe('c-hello-world', () => {
    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
    });

    it('renders default greeting', () => {
        const element = createElement('c-hello-world', { is: HelloWorld });
        document.body.appendChild(element);

        const paragraph = element.shadowRoot.querySelector('p');
        expect(paragraph.textContent).toBe('Hello, World!');
    });

    it('updates greeting on input change', () => {
        const element = createElement('c-hello-world', { is: HelloWorld });
        document.body.appendChild(element);

        return Promise.resolve().then(() => {
            const input = element.shadowRoot.querySelector('lightning-input');
            input.value = 'Roshan';
            input.dispatchEvent(new CustomEvent('change'));

            return Promise.resolve().then(() => {
                const paragraph = element.shadowRoot.querySelector('p');
                expect(paragraph.textContent).toBe('Hello, Roshan!');
            });
        });
    });
});
