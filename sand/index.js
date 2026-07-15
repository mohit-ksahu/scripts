// Hashes a text seed into a numeric value.
function fnv1a(seedString) {
  let hash = 2166136261;
  for (let i = 0; i < seedString.length; i++) {
    hash = Math.imul(hash ^ seedString.charCodeAt(i), 16777619);
  }
  return hash >>> 0;
}

// Seed-based random number generator.
function mulberry32(seed) {
  return () => {
    let value = seed += 0x6D2B79F5;
    value = Math.imul(value ^ (value >>> 15), value | 1);
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

// Converts HSL colors to hexadecimal.
function hslToHex(hue, saturation, lightness) {
  const factor = saturation * Math.min(lightness, 1 - lightness);
  const channel = (offset) => {
    const position = (offset + hue * 12) % 12;
    const color = lightness - factor * Math.max(
      Math.min(position - 3, 9 - position, 1),
      -1,
    );
    return Math.round(color * 255).toString(16).padStart(2, '0');
  };
  return '#' + channel(0) + channel(8) + channel(4);
}

// Shared export formats for SVG, Canvas, and Data URLs.
function draw(source, options = {}) {
  const padding = options.padding || 0;
  const background = options.background;
  const viewWidth = source.width + padding * 2;
  const viewHeight = source.height + padding * 2;

  return {
    svg() {
      let rects = '';
      source.each((x, y, color) => {
        rects += `<rect x="${padding + x}" y="${padding + y}" width="1" height="1" fill="${color}" />\n`;
      });
      let backgroundRect = '';
      if (background) {
        backgroundRect = `<rect width="${viewWidth}" height="${viewHeight}" fill="${background}" />\n`;
      }
      return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${viewWidth} ${viewHeight}" width="100%" height="100%" shape-rendering="crispEdges">\n${backgroundRect}${rects}</svg>`;
    },
    canvas(canvas, scale) {
      const context = canvas.getContext('2d');
      canvas.width = viewWidth * scale;
      canvas.height = viewHeight * scale;
      if (background) {
        context.fillStyle = background;
        context.fillRect(0, 0, canvas.width, canvas.height);
      }
      source.each((x, y, color) => {
        context.fillStyle = color;
        context.fillRect((padding + x) * scale, (padding + y) * scale, scale, scale);
      });
    },
    url() {
      const svg = this.svg();
      const bytes = new TextEncoder().encode(svg);
      const binString = Array.from(bytes, (byte) => String.fromCharCode(byte)).join('');
      return 'data:image/svg+xml;base64,' + btoa(binString);
    },
  };
}

// Generates the raw pattern layout.
function base(config) {
  const {seed, width, height, colors, density, symmetry} = config;
  const random = mulberry32(fnv1a(seed));

  const palette = Array.from({length: colors}, () => {
    return hslToHex(random(), random() * 0.4 + 0.5, random() * 0.3 + 0.4);
  });

  const map = Array.from({length: height}, () => Array(width).fill(null));

  if (symmetry) {
    for (const coordinates of symmetry) {
      if (random() < density) {
        const color = palette[Math.floor(random() * palette.length)];
        for (const coord of coordinates) {
          map[coord.y][coord.x] = color;
        }
      }
    }
  } else {
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        if (random() < density) {
          map[y][x] = palette[Math.floor(random() * palette.length)];
        }
      }
    }
  }

  const each = (callback) => {
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        if (map[y][x]) {
          callback(x, y, map[y][x]);
        }
      }
    }
  };

  const source = {seed, width, height, each};
  return {
    ...source,
    ...draw(source),
  };
}


// Extensions

// Rules for mirroring coordinates.
const symmetries = {
  horizontal(width, height) {
    const regions = [];
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < Math.ceil(width / 2); x++) {
        regions.push([{x, y}, {x: width - 1 - x, y}]);
      }
    }
    return regions;
  },
  vertical(width, height) {
    const regions = [];
    for (let y = 0; y < Math.ceil(height / 2); y++) {
      for (let x = 0; x < width; x++) {
        regions.push([{x, y}, {x, y: height - 1 - y}]);
      }
    }
    return regions;
  },
};

// Wrapper that adds padding and background styling.
function sand(config) {
  const {symmetry, padding, background} = config;

  const source = base({
    ...config,
    symmetry: symmetries[symmetry] ? symmetries[symmetry](config.width, config.height) : null,
  });

  return {
    ...source,
    ...draw(source, {padding, background}),
  };
}

// Generates a styled SVG Data URL shortcut.
sand.url = (seed) => {
  return sand({
    seed,
    width: 8,
    height: 8,
    colors: 2,
    density: 0.6,
    padding: 1,
  }).url();
};

export {symmetries, base as sand};
export default sand;