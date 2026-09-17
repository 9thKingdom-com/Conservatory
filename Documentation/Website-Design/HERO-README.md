# Website hero artwork for CIDCORE

Use `9thkingdom-hero-conservatory.png` as the hero background. It is a clean AI reconstruction of the artwork embedded in Website-Concept-01.png, not an exact original image layer or an Unreal screenshot.

Suggested server destination: `/assets/images/9thkingdom-hero-conservatory.png` (upload required; this URL is not live yet).

Keep the headline and buttons as HTML. Remove the existing gradient-only hero background and combine the image with a light darkening overlay where needed:

```css
.hero {
  background-image:
    linear-gradient(90deg, rgba(10,25,19,.55), rgba(10,25,19,0) 75%),
    url('/assets/images/9thkingdom-hero-conservatory.png');
  background-size: cover;
  background-position: center, 65% center;
}
@media (max-width: 640px) {
  .hero { background-position: center, 72% center; }
}
```

Tune the crop against the real hero dimensions on desktop and mobile. Check text contrast after loading the image. Retain a visible HTML “Concept art — in development” caption. This art does not change the game's approved architecture.

PNG is browser-compatible and supplied as the source master. For production delivery, CIDCORE can encode responsive WebP/AVIF versions and retain this PNG as the master.
