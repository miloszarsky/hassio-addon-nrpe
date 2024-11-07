# Specify the base image.
ARG BUILD_FROM

# Ignore a specific linting rule DL3006 which requires a pin in the FROM image.
# hadolint ignore=DL3006

# Use the base image specified by the BUILD_FROM argument.
FROM $BUILD_FROM

# Set the default shell to Bash and enable the pipefail option.
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Declare build-time variables with an optional default value for NODE_EXPORTER_VERSION.
ARG \
  BUILD_ARCH \

# Copy the contents of the 'rootfs' directory from the build context into the root directory of the image.
COPY rootfs /


RUN \
    # Install the 'tar' package using apk, without caching the package index locally.
    apk add --no-cache --update tar nrpe nagios-plugins-all \
    # Assign the value of BUILD_ARCH to a new variable ARCH.
    && ARCH="${BUILD_ARCH}" \
    # Check if the architecture is 'aarch64' and if so, set ARCH to 'arm64'.
    && if [ "${BUILD_ARCH}" = "aarch64" ]; then ARCH="arm64"; fi

# Reset the entry point of the image to an empty array.
# This means no default executable will be run when the container starts.
ENTRYPOINT []

# This add-on runs on the host pid namespace, making it impossible
# to use S6-Overlay. Therefore the init system is disabled at this point.
CMD ["/run.sh"]
