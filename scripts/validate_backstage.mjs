// Validate every Backstage entity in the repo against the real Backstage schemas:
//   catalog-info.yaml, backstage/templates/**/template.yaml, generated/catalog/*.yaml
// Usage: node scripts/validate_backstage.mjs [repoRoot]
import fs from 'fs';
import path from 'path';
import YAML from 'yaml';
import {
  entitySchemaValidator,
  makeValidator,
  componentEntityV1alpha1Validator,
  resourceEntityV1alpha1Validator,
  locationEntityV1alpha1Validator,
} from '@backstage/catalog-model';
import { templateEntityV1beta3Validator } from '@backstage/plugin-scaffolder-common';

const root = path.resolve(process.argv[2] || '.');
const generic = entitySchemaValidator();
// Naming rules (entity names, tags, annotation and label keys/values) live in a separate
// validator layer from the JSON schemas, and the catalog enforces both at ingestion time.
const names = makeValidator();

function checkMetadata(entity) {
  const m = entity.metadata ?? {};
  const problems = [];
  if (!names.isValidEntityName(m.name)) problems.push(`invalid metadata.name '${m.name}'`);
  if (m.namespace !== undefined && !names.isValidNamespace(m.namespace)) problems.push(`invalid namespace '${m.namespace}'`);
  for (const t of m.tags ?? []) if (!names.isValidTag(t)) problems.push(`invalid tag '${t}'`);
  for (const [k, v] of Object.entries(m.annotations ?? {})) {
    if (!names.isValidAnnotationKey(k)) problems.push(`invalid annotation key '${k}'`);
    if (!names.isValidAnnotationValue(v)) problems.push(`invalid annotation value for '${k}'`);
  }
  for (const [k, v] of Object.entries(m.labels ?? {})) {
    if (!names.isValidLabelKey(k)) problems.push(`invalid label key '${k}'`);
    if (!names.isValidLabelValue(v)) problems.push(`invalid label value for '${k}'`);
  }
  if (problems.length) throw new Error(problems.join('; '));
}

const kindValidators = {
  Component: componentEntityV1alpha1Validator,
  Resource: resourceEntityV1alpha1Validator,
  Location: locationEntityV1alpha1Validator,
  Template: templateEntityV1beta3Validator,
};

function* walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (['node_modules', '.git'].includes(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else yield p;
  }
}

const targets = [...walk(root)].filter((f) => {
  const rel = path.relative(root, f).split(path.sep).join('/');
  return rel === 'catalog-info.yaml' || /^backstage\/templates\/.+\/template\.yaml$/.test(rel) || /^generated\/catalog\/.+\.yaml$/.test(rel);
});

let bad = 0, total = 0;
for (const file of targets.sort()) {
  const rel = path.relative(root, file);
  for (const doc of YAML.parseAllDocuments(fs.readFileSync(file, 'utf8'))) {
    if (doc.errors.length) { bad++; console.log('FAIL', rel, 'YAML:', doc.errors[0].message); continue; }
    const entity = doc.toJS();
    if (!entity) continue;
    total++;
    const label = `${rel} (${entity.kind}/${entity.metadata?.name})`;
    try {
      generic(entity);
      checkMetadata(entity);
      const kv = kindValidators[entity.kind];
      if (!kv) throw new Error(`no validator for kind ${entity.kind}`);
      const ok = await kv.check(entity);
      if (!ok) throw new Error('kind validator rejected the entity');
      console.log('OK  ', label);
    } catch (e) {
      bad++;
      console.log('FAIL', label, String(e.message || e).split('\n')[0]);
    }
  }
}
console.log(`${total - bad}/${total} entities valid`);
process.exit(bad || total === 0 ? 1 : 0);
