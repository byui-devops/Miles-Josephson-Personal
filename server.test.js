const request = require('supertest');
const app = require('./server');

describe('GET /health', () => {
  test('returns 200 with status ok', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body).toEqual({ status: 'ok' });
  });
});

describe('GET /validate-age/:age', () => {
  test('returns valid=true for a valid age (25)', async () => {
    const res = await request(app).get('/validate-age/25');
    expect(res.statusCode).toBe(200);
    expect(res.body.valid).toBe(true);
    expect(res.body.age).toBe(25);
  });

  test('returns valid=true for minimum valid age (18)', async () => {
    const res = await request(app).get('/validate-age/18');
    expect(res.statusCode).toBe(200);
    expect(res.body.valid).toBe(true);
  });

  test('returns valid=false for underage value (17)', async () => {
    const res = await request(app).get('/validate-age/17');
    expect(res.statusCode).toBe(200);
    expect(res.body.valid).toBe(false);
  });

  test('returns valid=false for overage value (121)', async () => {
    const res = await request(app).get('/validate-age/121');
    expect(res.statusCode).toBe(200);
    expect(res.body.valid).toBe(false);
  });

  test('returns valid=false for non-numeric age string', async () => {
    const res = await request(app).get('/validate-age/abc');
    expect(res.statusCode).toBe(200);
    expect(res.body.valid).toBe(false);
  });
});
