import { Stack } from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export function createTable(stack: Stack, id: string, pk: string) {
    let table = new dynamodb.Table(stack, id, {
        partitionKey: {name: pk, type: dynamodb.AttributeType.STRING},

    });
    return table
}