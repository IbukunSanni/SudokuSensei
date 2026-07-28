import assert from "node:assert/strict";
import test from "node:test";
import {
  componentCorners,
  computeAdaptiveMask,
  findLargestComponent,
  projectPoint,
  unitSquareToQuadrilateral,
} from "../src/utils/imageGridProcessing.mjs";

test("adaptive threshold identifies a dark line against a light image", () => {
  const gray = new Uint8ClampedArray(25).fill(240);
  for (let row = 0; row < 5; row++) gray[row * 5 + 2] = 20;
  const mask = computeAdaptiveMask(gray, 5, 5, 2, 5);
  assert.equal(mask[2], 1);
  assert.equal(mask[0], 0);
});

test("finds the largest connected component and its ordered corners", () => {
  const mask = new Uint8Array(64);
  for (let y = 2; y <= 5; y++) {
    for (let x = 2; x <= 5; x++) mask[y * 8 + x] = 1;
  }
  mask[0] = 1;
  const component = findLargestComponent(mask, 8, 8);
  assert.equal(component.length, 16);
  assert.deepEqual(componentCorners(component, 8), [
    { x: 2, y: 2 },
    { x: 5, y: 2 },
    { x: 5, y: 5 },
    { x: 2, y: 5 },
  ]);
});

test("homography maps square corners onto a photographed quadrilateral", () => {
  const corners = [
    { x: 12, y: 20 },
    { x: 92, y: 8 },
    { x: 100, y: 110 },
    { x: 4, y: 96 },
  ];
  const transform = unitSquareToQuadrilateral(corners);
  const projected = [
    projectPoint(transform, 0, 0),
    projectPoint(transform, 1, 0),
    projectPoint(transform, 1, 1),
    projectPoint(transform, 0, 1),
  ];
  projected.forEach((point, index) => {
    assert.ok(Math.abs(point.x - corners[index].x) < 1e-6);
    assert.ok(Math.abs(point.y - corners[index].y) < 1e-6);
  });
});
