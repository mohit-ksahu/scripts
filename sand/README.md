# Sand

A lightweight JavaScript library to generate unique pixel art patterns and avatars from text. 

Whether you need placeholder profile pictures, abstract game graphics, or unique visual designs, Sand turns any word or name into a beautiful, consistent layout.

### Highlights
* **Seed-based**: The same text seed always generates the exact same pattern.
* **Highly customizable**: Easily control colors, fill density, border padding, and background styling.
* **Mirroring options**: Use built-in horizontal and vertical symmetry, or define your own coordinates.
* **Modern formats**: Export directly as SVG, draw onto HTML5 Canvas, or generate a link to load in `<img>` tags.
* **Lightweight**: Built in a single file (`index.js`) with zero external dependencies.

## How to use

### Base version (no background or padding)

```javascript
import { sand } from './index.js';

const image = sand({
  seed: 'sand',
  width: 10,
  height: 10,
  colors: 3,
  density: 0.75,
  symmetry: null, // Custom coordinates array (optional)
});
```

### Styled version (with background, padding, and built-in symmetry)

```javascript
import sand from './index.js';

const styled = sand({
  seed: 'sand',
  width: 10,
  height: 10,
  colors: 3,
  density: 0.75,
  padding: 1,
  background: '#ffffff',
  symmetry: 'horizontal',
});
```

### Options

| Name | Type | Description |
| :--- | :--- | :--- |
| `seed` | `string` | Text used to generate the pattern. |
| `width` | `number` | Width of the image. |
| `height` | `number` | Height of the image. |
| `colors` | `number` | Number of colors to use. |
| `density` | `number` | How full the pattern is (from `0.0` to `1.0`). |
| `symmetry` | `array` | Custom mirroring coordinates (optional). |

### Styling Options

| Name | Type | Description |
| :--- | :--- | :--- |
| `padding` | `number` | Blank border space around the image. |
| `background` | `string` | Background color (hex). |
| `symmetry` | `string` | Mirror mode (`'horizontal'` or `'vertical'`). |

### Image Methods

*   **`image.svg()`**: Returns the SVG image text.
*   **`image.canvas(canvas, scale)`**: Draws the pattern onto a canvas element.
*   **`image.url()`**: Returns a link to put directly inside `<img src="...">`.
*   **`image.each(callback)`**: Loops over every colored pixel: `(x, y, color) => {}`.

### Helpers

*   **`sand.url(seed)`**: Directly generates a styled avatar link from a text string.

## Running the App

To open the app in your browser:

```bash
npx serve .
```
