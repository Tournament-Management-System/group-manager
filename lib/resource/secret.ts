import { Stack } from 'aws-cdk-lib';
import * as secrets from 'aws-cdk-lib/aws-secretsmanager'
export function createSecret(stack: Stack, stage: string) {
    const secret = new secrets.Secret(stack, 'trounamentCreds', {
        description: 'example of createSecret',
        secretName: `tournamentManagement/${stage}`
    });
    return secret;
}