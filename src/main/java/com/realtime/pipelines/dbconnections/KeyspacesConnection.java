package com.realtime.pipelines.dbconnections;

import com.datastax.oss.driver.api.core.CqlSession;
import com.datastax.oss.driver.api.core.config.DriverConfigLoader;
import com.datastax.oss.driver.api.core.cql.ResultSet;
import com.datastax.oss.driver.api.core.cql.Row;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.AwsCredentialsProvider;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;

import java.net.InetSocketAddress;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.Collections;
import java.util.List;

public class KeyspacesConnection implements AutoCloseable {
    private final CqlSession session;

    public KeyspacesConnection(String awsAccessKeyId, String awsSecretAccessKey, Region awsRegion, String keyspace, String sslCertPath) {
        // Configure AWS credentials using basic credentials
        AwsBasicCredentials awsCredentials = AwsBasicCredentials.create(awsAccessKeyId, awsSecretAccessKey);
        // Create an AWS KeySpaces client
        AwsCredentialsProvider credentialsProvider = StaticCredentialsProvider.create(awsCredentials);

        // Resolve el punto de contacto y crea la sesión
        /*InetSocketAddress contactPoint = resolveContactPoint("cassandra.us-east-1.amazonaws.com");*/
        List<InetSocketAddress> contactPoints =
                Collections.singletonList(
                        InetSocketAddress.createUnresolved("cassandra.us-east-1.amazonaws.com", 9142));

        DriverConfigLoader loader = DriverConfigLoader.fromClasspath("application.conf");
        try {
            this.session = CqlSession.builder()
                    .addContactPoints(contactPoints)
                    .withKeyspace(keyspace)
                    .withConfigLoader(loader)
                    .build();
            ResultSet rs = session.execute("select * from system_schema.keyspaces");
            Row row = rs.one();
            System.out.println(row.getString("keyspace_name"));
        } catch (Exception e) {
            throw new RuntimeException("Error al establecer la conexión a Keyspaces AWS");
        }
    }
    private InetSocketAddress resolveContactPoint(String hostName) {
        try {
            InetAddress inetAddress = InetAddress.getByName(hostName);
            return new InetSocketAddress(inetAddress, 9142); // El puerto 9142 es el puerto SSL por defecto de Amazon Keyspaces.
        } catch (UnknownHostException e) {
            throw new RuntimeException("Error al resolver el punto de contacto.", e);
        }
    }

    public CqlSession getSession() {
        return session;
    }

    @Override
    public void close() {

        if (session != null){
            session.close();
        }
    }
}