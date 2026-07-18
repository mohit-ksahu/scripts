import sand from './index.min.js';

const $ = (id) => document.getElementById(id);
const seedInput = $('seed-input');
const btnRand = $('btn-rand');
const widthInput = $('width-input');
const heightInput = $('height-input');
const colorsInput = $('colors-input');
const paddingInput = $('padding-input');
const densityInput = $('density-input');
const symmetrySelect = $('symmetry-select');
const bgEnabled = $('bg-enabled');
const bgColorInput = $('bg-color-input');
const previewBox = $('preview-box');
const btnSvg = $('btn-svg');
const btnPng = $('btn-png');
const btnDataUrl = $('btn-dataurl');
const codeOutput = $('code-output');

let current = null;
const randomString = () => Math.random().toString(36).substring(2, 10);

const getConfig = () => ({
  seed: seedInput.value,
  width: parseInt(widthInput.value, 10),
  height: parseInt(heightInput.value, 10),
  colors: parseInt(colorsInput.value, 10),
  padding: parseInt(paddingInput.value, 10),
  density: parseInt(densityInput.value, 10) / 100,
  background: bgEnabled.checked ? bgColorInput.value : null,
  symmetry: symmetrySelect.value === 'raw' ? null : symmetrySelect.value,
});

const renderPreview = () => {
  const config = getConfig();
  current = sand(config);
  previewBox.innerHTML = current.svg();

  const symmetryPart = symmetrySelect.value === 'raw'
    ? ''
    : `,\n  symmetry: '${symmetrySelect.value}'`;
  const bgPart = config.background
    ? `,\n  background: '${config.background}'`
    : '';

  codeOutput.value = `sand({
  seed: '${config.seed}',
  width: ${config.width},
  height: ${config.height},
  colors: ${config.colors},
  padding: ${config.padding},
  density: ${config.density}${bgPart}${symmetryPart}
});`;
  codeOutput.style.height = 'auto';
  codeOutput.style.height = `${codeOutput.scrollHeight}px`;
};

const download = (url, filename) => {
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

btnRand.addEventListener('click', () => {
  seedInput.value = randomString();
  renderPreview();
});

const inputs = [
  seedInput, widthInput, heightInput, colorsInput,
  paddingInput, densityInput, symmetrySelect, bgEnabled, bgColorInput,
];
for (const el of inputs) {
  el.addEventListener('input', renderPreview);
}

btnSvg.addEventListener('click', () => {
  const blob = new Blob([current.svg()], {type: 'image/svg+xml;charset=utf-8'});
  const url = URL.createObjectURL(blob);
  download(url, `${current.seed}.svg`);
  URL.revokeObjectURL(url);
});

btnPng.addEventListener('click', () => {
  const canvas = document.createElement('canvas');
  const size = Math.max(current.width, current.height);
  current.canvas(canvas, Math.max(1, Math.floor(1024 / size)));
  download(canvas.toDataURL('image/png'), `${current.seed}.png`);
});

btnDataUrl.addEventListener('click', () => {
  navigator.clipboard.writeText(current.url()).then(() => {
    const originalText = btnDataUrl.textContent;
    btnDataUrl.textContent = 'Copied!';
    setTimeout(() => btnDataUrl.textContent = originalText, 1500);
  });
});

seedInput.value = randomString();
renderPreview();