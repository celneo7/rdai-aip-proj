const exampleForm = document.querySelector('#example-form');
const uploadForm = document.querySelector('#upload-form');
const examples = document.querySelector('#examples');
const audio = document.querySelector('#audio');
const status = document.querySelector('#status');
const results = document.querySelector('#results');
const source = document.querySelector('#source');
let examplesReady = false;

function updateSource() {
  exampleForm.hidden = source.value !== 'example';
  uploadForm.hidden = source.value !== 'upload';
  results.hidden = true;
  message('');
}

source.addEventListener('change', updateSource);
updateSource();

function message(text, error = false) {
  status.textContent = text;
  status.classList.toggle('error', error);
}

async function readResponse(response) {
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(typeof data?.detail === 'string' ? data.detail : `Request failed (${response.status}).`);
  }
  if (!data) throw new Error('Unexpected server response.');
  return data;
}

async function loadExamples() {
  try {
    const data = await readResponse(await fetch('/examples'));
    examples.replaceChildren(new Option('Select an example', ''));
    for (const item of data.audio_files) examples.add(new Option(item.filename, item.filename));
    examplesReady = data.audio_files.length > 0;
    examples.disabled = !examplesReady;
    exampleForm.querySelector('button').disabled = !examplesReady;
    if (!examplesReady) message('No examples available. You can still upload audio.');
  } catch (error) {
    examples.replaceChildren(new Option('Examples unavailable', ''));
    message(`Could not load examples: ${error.message} You can still upload audio.`, true);
  }
}

function displayResult(data) {
  document.querySelector('#info').textContent = `${data.filename} · Language: ${data.metadata.language}`;
  document.querySelector('#transcript').textContent = data.metadata.text || 'No speech recognised.';
  const segments = document.querySelector('#segments');
  segments.replaceChildren();
  for (const segment of data.metadata.segments) {
    const item = document.createElement('li');
    item.textContent = `[${segment.start.toFixed(2)}s → ${segment.end.toFixed(2)}s] ${segment.text}`;
    segments.append(item);
  }
  results.hidden = false;
}

async function transcribe(url, options) {
  const controls = document.querySelectorAll('button, input, select');
  controls.forEach(control => { control.disabled = true; });
  results.hidden = true;
  message('Transcribing… This may take a moment.');
  try {
    displayResult(await readResponse(await fetch(url, options)));
    message('Transcription complete.');
  } catch (error) {
    message(error.message, true);
  } finally {
    controls.forEach(control => { control.disabled = false; });
    examples.disabled = !examplesReady;
    exampleForm.querySelector('button').disabled = !examplesReady;
  }
}

exampleForm.addEventListener('submit', event => {
  event.preventDefault();
  transcribe('/transcribe-example', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ filename: examples.value }),
  });
});

uploadForm.addEventListener('submit', event => {
  event.preventDefault();
  const file = audio.files[0];
  if (!file) return message('Choose a file first.', true);
  if (file.size > 25 * 1024 * 1024) return message('File exceeds the 25 MiB limit.', true);
  const body = new FormData();
  body.append('file', file);
  // Let the browser set the multipart Content-Type and boundary.
  transcribe('/transcribe', { method: 'POST', body });
});

loadExamples();
