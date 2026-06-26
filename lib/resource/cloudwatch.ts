import { RemovalPolicy, Stack } from 'aws-cdk-lib';
import { LogGroup, RetentionDays } from 'aws-cdk-lib/aws-logs';

export function createLogGroup(stack: Stack, id: string) {
    const loggroup = new LogGroup(stack, id, {
        logGroupName: `tournamentManagement/${id}`,
        removalPolicy: RemovalPolicy.DESTROY,
        retention: RetentionDays.ONE_MONTH
    })
    return loggroup;
}